#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)

# TODO: connect to a local postgresql database
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String())
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    venue_shows = db.relationship('Shows', backref="venue_shows")

    def __repr__(self):
      return f'<Venue {self.id}, name: {self.name}, city: {self.city}, state: {self.state}>'

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    artist_shows = db.relationship('Shows', backref="artist_shows")

    def __repr__(self):
      return f'<Artist {self.id}, name: {self.name}>'
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
  time = db.Column(db.String(), nullable=False)
  
  def __repr__(self):
      return f'<Show {self.id}>'
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

def create_genre_arr(string):
  genres = []
  genre = ""   
  for ltr in string:
    if ltr == "{" or ltr == "\"":
      continue
    elif ltr == "," or ltr == "}":
        genres.append(genre)
        genre = ""
        continue
    genre += ltr
  return genres

def get_past_shows(show_arr):
  past_shows = []
  current_time = datetime.now()
  for show in show_arr:
    show_time = datetime.strptime(show.time, '%Y-%m-%d %H:%M:%S')
    if show_time <= current_time:
      past_shows.append(show)
  return past_shows

def get_upcoming_shows(show_arr):
  upcoming_shows = []
  current_time = datetime.now()
  for show in show_arr:
    show_time = datetime.strptime(show.time, '%Y-%m-%d %H:%M:%S')
    if show_time > current_time:
      upcoming_shows.append(show)
  return upcoming_shows

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  visited = set()
  data = []
  all_venues = Venue.query.all()

  for venue in all_venues:
    city = venue.city
    state = venue.state
    if (city, state) in visited:
      continue
    visited.add((city, state))
    venues_by_city = Venue.query.filter_by(city=city, state=state).all()
    
    city_venue = {}
    city_venue['city'] = city
    city_venue['state'] = state
    city_venue['venues'] = []

    for venue in venues_by_city:
      venue_data = {}
      venue_data['id'] = venue.id
      venue_data['name'] = venue.name
      venue_data['num_upcoming_shows'] = len(get_upcoming_shows(venue.venue_shows))
      city_venue['venues'].append(venue_data)
    data.append(city_venue)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', '')
  all_venues = Venue.query.all()
  response = {}
  response['count'] = 0
  response['data'] = []

  for venue in all_venues:
    if search_term.lower() in venue.name.lower():
      venue_data = {}
      venue_data['id'] = venue.id
      venue_data['name'] = venue.name
      venue_data['num_upcoming_shows'] = len(get_upcoming_shows(venue.venue_shows))
      response['count'] += 1
      response['data'].append(venue_data)

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  def get_shows_info(show_arr):
    shows = []
    for show in show_arr:
      show_dict = {}
      artist = Artist.query.get(show.artist_id)
      show_dict['artist_id'] = show.artist_id
      show_dict['artist_name'] = artist.name
      show_dict['artist_image_link'] = artist.image_link
      show_dict['start_time'] = show.time
      shows.append(show_dict)
    return shows
  error = False
  try:
    venue = Venue.query.get(venue_id)
    shows = db.session.query(Shows).join(Venue, venue_id == Shows.venue_id).all()
    past_shows = get_past_shows(shows)
    upcoming_shows = get_upcoming_shows(shows)
    data = {}
    data['id'] = venue.id
    data['name'] = venue.name
    data['genres'] = create_genre_arr(venue.genres)
    data['address'] = venue.address
    data['city'] = venue.city
    data['state'] = venue.state
    data['phone'] = venue.phone
    data['website'] = venue.website
    data['facebook_link'] = venue.facebook_link
    data['seeking_talent'] = venue.seeking_talent
    data['seeking_description'] = venue.seeking_description
    data['image_link'] = venue.image_link
    data['past_shows'] = get_shows_info(past_shows)
    data['upcoming_shows'] = get_shows_info(upcoming_shows)
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
  except:
    error = True
    print(sys.exc_info())
  if error:
    abort(400)


  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  error = False
  venue = Venue(name=request.form['name'], genres=request.form['genres'], address=request.form['address'], city=request.form['city'],  
  state=request.form['state'], phone=request.form['phone'], facebook_link=request.form['facebook_link'])
  try:
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback
  finally:
    db.session.close()
  
  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  if error:
    flash('An error occured. Venue ' + venue.name + ' could not be listed.')
    abort(400)

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback
  finally:
    db.session.close()
  if error:
    abort(400)
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    artist_data = {}
    artist_data['id'] = artist.id
    artist_data['name'] = artist.name
    data.append(artist_data)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')
  all_artists = Artist.query.all()
  response = {}
  response['count'] = 0
  response['data'] = []

  for artist in all_artists:
    if search_term.lower() in artist.name.lower():
      artist_data = {}
      artist_data['id'] = venue.id
      artist_data['name'] = venue.name
      artist_data['num_upcoming_shows'] = artist.upcoming_shows_count
      response['count'] += 1
      response['data'].append(artist_data)
  
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artists table, using artist_id

  def get_shows_info(show_arr):
    shows = []
    for show in show_arr:
      show_dict = {}
      venue = Venue.query.get(show.venue_id)
      show_dict['venue_id'] = show.venue_id
      show_dict['venue_name'] = venue.name
      show_dict['venue_image_link'] = venue.image_link
      show_dict['start_time'] = show.time
      shows.append(show_dict)
    return shows

  error = False
  try: 
    artist = Artist.query.get(artist_id)
    shows = db.session.query(Shows).join(Artist, artist_id == Shows.artist_id).all()
    past_shows = get_past_shows(shows)
    upcoming_shows = get_upcoming_shows(shows)
    data = {}
    data['id'] = artist.id
    data['name'] = artist.name
    data['genres'] = create_genre_arr(artist.genres)
    data['city'] = artist.city
    data['state'] = artist.state
    data['phone'] = artist.phone
    data['website'] = artist.website
    data['facebook_link'] = artist.facebook_link
    data['seeking_venue'] = artist.seeking_venue
    data['seeking_description'] = artist.seeking_description
    data['image_link'] = artist.image_link
    data['past_shows'] = get_shows_info(past_shows)
    data['upcoming_shows'] = get_shows_info(upcoming_shows)
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
  except:
    error = True
    print(sys.exc_info())
  if error:
    abort(400)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  artist = Artist.query.get(artist_id)

  artist.name = request.form['name']
  artist.genres = request.form['genres']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.facebook_link = request.form['facebook_link']

  try:
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback
  finally:
    db.session.close()
  if error:
    abort(400)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  venue = Venue.query.get(venue_id)
  venue.name = request.form['name']
  venue.genres = request.form['genres']
  venue.address = request.form['address']
  venue.city = request.form['city']
  venue.state = request.form['state']
  venue.phone = request.form['phone']
  venue.facebook_link = request.form['facebook_link']

  try:
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback
  finally:
    db.session.close()
  if error:
    abort(400)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  artist = Artist(name=request.form['name'], genres=request.form['genres'], city=request.form['city'],  
  state=request.form['state'], phone=request.form['phone'], facebook_link=request.form['facebook_link'])
  try:
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  if error:
    flash('An error occured. Artist ' + artist.name + ' could not be listed.')
    abort(400)

  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  shows = Shows.query.all()
  data = []
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    show_data = {}
    show_data['venue_id'] = venue.id
    show_data['venue_name'] = venue.name
    show_data['artist_name'] = artist.name
    show_data['artist_image_link'] = artist.image_link 
    show_data['start_time'] = show.time
    data.append(show_data)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  show = Shows(name=request.form['artist_id'], venue_id=request.form['venue_id'], city=request.form['start_time'])

  try:
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  if error:
    flash('An error occured. Show could not be listed.')
    abort(400)
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
