#===: JUST FOR ADMIN :===
from server import app, db, Game;

with app.app_context():
    g1 = Game(
        alias="roulette",
        name="Ruleta del Inca",
        description="Recibe el botín Inca apostando por tus números de la suerte.",
        imageGame="static/img/cardRoulette.png",
    );
    db.session.add(g1);
    g2 = Game(
        alias="slots",
        name="Fortuna del Sol",
        description="Obtén 3 figuras idénticas y prepárate para ganar hasta S/.100,000!",
        imageGame="static/img/cardSlots.png",
    );
    db.session.add(g2);
    
    db.session.commit();
    db.create_all();