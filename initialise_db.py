from project import db, create_app
from project.models import Photo, User


def populate_db():
  session = db.session()

  # Creat a dummy admin user
  # username: admin
  # password: adminpass
  user = User(username = "admin")
  user.set_password("admin")
  user.set_admin()
  
  session.add(user)
  session.commit()

  # Create a photo array instead of adding them one by one to the db
  # Note: each photo now has a user_id value required now
  photos = [
    Photo(
      name = "William Warby",
      caption = "Gentoo penguin",
      description = "A penguin with an orange beak standing next to a rock.",
      file = "williamA.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Javier Patino Loira",
      caption = "Common side-blotched lizard",
      description = "A close up of a lizard on a rock.",
      file = "javier.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Jordie Rubies",
      caption = "Griffin vulture flying",
      description = "A large bird flying through a blue sky.",
      file = "jordi.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Jakub Neskora",
      caption = "Jaguar",
      description = "A close up of a leopard near a rock.",
      file = "jakub.jpg",
      user_id = user.id
    ),
    Photo(
      name = "William Warby",
      caption = "Japanese macaque",
      description = "A monkey sitting on top of a wooden post.",
      file = "williamB.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Hanvin Cheong",
      caption = "Nakano",
      description = "A group of people walking across a street.",
      file = "hanvin.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Ekaterina Bogdan",
      caption = "Bologna",
      description = "A bike parked next to a pole.",
      file = "ekaterina.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Dima DallAcqua",
      caption = "Alcatraz Island",
      description = "A close up of a green plant.",
      file = "dima.jpg",
      user_id = user.id
    ),
    Photo(
      name = "Edgar",
      caption = "Oporto, Portugal",
      description = "A man sitting on a bench at a train station.",
      file = "edgar.jpg",
      user_id = user.id
    )
  ]

  # Save the photo array to the DB and commit the changes
  session.bulk_save_objects(photos)
  session.commit()

# Run create_app(), clear the DB and run populate_db()
if __name__ == "__main__":
  app = create_app()
  with app.app_context():
    db.drop_all()
    db.create_all()
    populate_db()
