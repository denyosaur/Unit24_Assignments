from models import Pet, db
from app import app

'''clear db and remake models table'''
db.drop_all()
db.create_all()

Pet.query.delete()

Whiskers = Pet(name='Whiskers', species='Kitty', photo_url='https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg', age=3, notes='Good cat', available=True)
Doge = Pet(name='Doge', species='Doge', photo_url='https://crhscountyline.com/wp-content/uploads/2020/03/Capture.png', age=6, notes='much amaze', available=True)
Raisin = Pet(name='Raisin', species='Racoon', photo_url='https://extension.umd.edu/sites/extension.umd.edu/files/resize/_images/programs/hgic/wildlife/raccoon-1905528_640-498x346.jpg', age=4, notes='Loves Trash', available=True)
Ronald = Pet(name='Ronald', species='Deer', photo_url='https://wehco.media.clients.ellingtoncms.com/img/photos/2019/06/17/resized_250499-1b-deer-0618_85-26607.JPG', age=10, notes='Quiet Deer', available=False)

db.session.add(Whiskers)
db.session.add(Doge)
db.session.add(Raisin)
db.session.add(Ronald)

db.session.commit()