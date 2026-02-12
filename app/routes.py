from flask import Blueprint, render_template, redirect, url_for
from .models import Feed, Trash, Walk, OptionalTask
from . import db
from flask import request, jsonify
import datetime

bp = Blueprint("main", __name__)

DOGS = ["てつ"]
CATS = ["ぽんず"]

TIMES_DOG = ["朝", "昼", "夜"]
TIMES_CAT = ["朝", "昼", "夜"]

OPTIONAL_TASKS = [
    "朝てつんぽ",
    "夜てつんぽ",
    "ゴミ出し",
    "洗濯物", 
    "リビング点灯", 
    "ぽんずトイレ"
]


@bp.route("/initdb")
def initdb():
    db.create_all()
    return "✅ Tables created"

@bp.route("/bulk_update", methods=["POST"])
def bulk_update():
    today = datetime.date.today().isoformat()
    data = request.get_json()

    for key, value in data.items():
        typ, *rest = key.split("|")
        if typ == "feed":
            dog, time = rest
            rec = Feed.query.filter_by(date=today, dog=dog, time=time).first()
            if rec:
                rec.fed = value
        elif typ == "task":
            task = rest[0]
            rec = OptionalTask.query.filter_by(date=today, name=task).first()
            if rec:
                if task == "ぽんずトイレ":
                    rec.count += 1
                    rec.done = True
                else:
                    rec.done = value


    db.session.commit()
    return {"ok": True}


def clean_old_data():
    today = datetime.date.today().isoformat()
    db.session.query(Feed).filter(Feed.date != today).delete()
    db.session.query(Trash).filter(Trash.date != today).delete()
    db.session.query(Walk).filter(Walk.date != today).delete()
    db.session.commit()


@bp.route("/")
def index():
    db.create_all()
    today = datetime.date.today().isoformat()
    clean_old_data()

    # 犬の初期化
    for dog in DOGS:
        for t in TIMES_DOG:
            if not Feed.query.filter_by(date=today, dog=dog, time=t).first():
                db.session.add(Feed(date=today, dog=dog, time=t, fed=False))

    # 猫の初期化
    for cat in CATS:
        for t in TIMES_CAT:
            if not Feed.query.filter_by(date=today, dog=cat, time=t).first():
                db.session.add(Feed(date=today, dog=cat, time=t, fed=False))

    # 通常業務
    for task in OPTIONAL_TASKS:
        if not OptionalTask.query.filter_by(date=today, name=task).first():
            db.session.add(OptionalTask(date=today, name=task, done=False))

    if not Trash.query.filter_by(date=today).first():
        db.session.add(Trash(date=today, taken=False))

    if not Walk.query.filter_by(date=today).first():
        db.session.add(Walk(date=today, taken=False))

    db.session.commit()

    feeds = Feed.query.filter_by(date=today).all()
    state = {(f.dog, f.time): f.fed for f in feeds}

    optionals = OptionalTask.query.filter_by(date=today).all()
    optional_state = {o.name: o.done for o in optionals}

    return render_template(
        "index.html",
        today=today,
        state=state,
        TIMES_DOG=TIMES_DOG,
        TIMES_CAT=TIMES_CAT,
        DOGS=DOGS,
        CATS=CATS,
        OPTIONAL_TASKS=OPTIONAL_TASKS,
        optional_state=optional_state,
        optionals=optionals      # ← これを追加
    )


@bp.route("/toggle/<dog>/<time>")
def toggle(dog, time):
    today = datetime.date.today().isoformat()
    feed = Feed.query.filter_by(date=today, dog=dog, time=time).first()
    feed.fed = not feed.fed
    db.session.commit()
    return redirect(url_for("main.index"))


@bp.route("/toggle_optional/<task>")
def toggle_optional(task):
    today = datetime.date.today().isoformat()
    record = OptionalTask.query.filter_by(date=today, name=task).first()
    record.done = not record.done
    db.session.commit()
    return redirect(url_for("main.index"))

