from app.joboffers import joboffer_blueprint
from flask import render_template, g, request, redirect, url_for, session
from flask_login import login_required
from app.joboffers.forms import OfferForm
from app.joboffers.dao import Joboffer





@joboffer_blueprint.route('/add_offer/', methods=['GET', 'POST'])
@login_required
def add_offer():
    form = OfferForm()
    if request.method == 'POST':
        g.con_psql.insert_joboffer_rec(g.user.get_id(),
                                          request.values.get('description'),
                                          request.values.get('skills'),
                                          request.values.get('title')
        )
        return redirect(url_for('authorization_blueprint.profile'))

    return render_template('add_new_offer.html', form=form)


@joboffer_blueprint.route('/offer/<string:id>')
@login_required
def user_offer(id):
    user_offers_info = g.con_psql.get_user_offers_info(id)
    return render_template('user_offer.html', user_offer=user_offers_info)



@joboffer_blueprint.route('/my_favorites/<string:id>', methods=['GET', 'POST'])
@login_required
def offer_edit(id):
    form = OfferForm()
    user_offers_info = [Joboffer(offer['id'], offer['author'], offer['title'], offer['offer_description'], offer['slill_list']) for offer in g.con_psql.get_user_offers_info(id)][0]
    if request.method == 'POST':
        g.con_psql.update_joboffer_rec(   g.user.get_id(),
                                          request.values.get('description'),
                                          request.values.get('skills'),
                                          request.values.get('title'),
                                          id
        )
        return redirect(url_for('authorization_blueprint.profile'))

    return render_template('offer_edit.html', offer = user_offers_info, form=form)



@joboffer_blueprint.route('/my_favorites/', methods=['GET', 'POST'])
@login_required
def user_favorites():

    if request.method == 'POST':
            if request.values.get("delete") is not None:
                g.con_psql.del_user_favorites(g.user.get_id(), request.values.get("delete"))

    all_resumes = [
        Joboffer(offer['id'], offer['author'], offer['title'], offer['offer_description'], offer['slill_list']) for
        offer in g.con_psql.get_user_favorites_datail(g.user.get_id())]

    return render_template('user_favorites.html', resumes=all_resumes)


@joboffer_blueprint.route('/jobs/', methods=['GET', 'POST'])
@joboffer_blueprint.route('/resumes/', methods=['GET', 'POST'])
@login_required
def all_resumes():
    type = 1 if request.path == '/offers/jobs/' else 0
    link_search = '/offers/jobs/' if request.path == '/offers/jobs/' else '/offers/resumes/'
    session['url'] = link_search

    args = request.args
    all_resumes = [Joboffer(offer['id'], offer['author'], offer['title'], offer['offer_description'], offer['slill_list']) for offer in g.con_psql.get_all_offers_info(type)]

    #g.user.get_id()
    #if g.user.get_account_type() != all_resumes[0].author_id:
    #    print('True')

    if request.method == 'POST':
        if request.values.get("unlike") is not None:
            g.con_psql.add_user_favorites(g.user.get_id(), request.values.get("unlike"))
        if request.values.get("like") is not None:
            g.con_psql.del_user_favorites(g.user.get_id(), request.values.get("like"))

    favorites = [fav['id_offer'] for fav in g.con_psql.get_user_favorites(g.user.get_id())]


    if args.get('search') == '' or args.get('search') is None:
        return render_template('resumes.html', resumes=all_resumes, favorites=favorites, link_search=link_search, type=type)

    for item in all_resumes:
        match_count = item.search_offer(args.get('search'))
        if match_count is None:
            all_resumes.remove(item)
    if match_count is None and len(all_resumes) == 1:
        all_resumes = None
    else:
        all_resumes = sorted(all_resumes, key=lambda x: x.score)


    return render_template('resumes.html', resumes=all_resumes, favorites=favorites, link_search=link_search, type=type, old_search=args.get('search'))

