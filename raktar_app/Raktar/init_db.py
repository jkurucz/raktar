﻿from __future__ import annotations

from app import db
from app import create_app
from config import Config

app = create_app(config_class=Config)

app.app_context().push()

#Role
from app.models.role import Role

# db.session.add_all([ Role(name="Administrator"), 
#                      Role(name="Chef"), 
#                      Role(name = "Courier"), 
#                      Role(name ="User") ])
# db.session.commit()


#Address
from app.models.address import Address

#db.session.add(Address( city = "Veszprém",  street = "Egyetem u. 1", postalcode=8200))
#db.session.commit()


#User
from app.models.user import User, UserRestaurant, UserRole

# user = User(name="Test User", email="test@gmail.com", phone="+3620111111")
# user.address = db.session.get(Address, 1)
# user.set_password("qweasd")

# db.session.add(user)

# u = db.session.get(User, 1)
# u.roles.append(db.session.get(Role,2))
# u.roles.append(db.session.get(Role,4))

#db.session.commit()

