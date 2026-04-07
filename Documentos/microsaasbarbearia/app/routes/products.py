import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.product import Product

products_bp = Blueprint("products", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@products_bp.route("/produtos")
@login_required
@tenant_required
def index():
    shop_id = current_user.barber_shop_id
    search = request.args.get("q", "").strip()
    query = Product.query.filter_by(barber_shop_id=shop_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    products = query.order_by(Product.created_at.desc()).all()
    return render_template("products/index.html", products=products, search=search)


@products_bp.route("/produtos/criar", methods=["POST"])
@login_required
@tenant_required
def create():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    price = request.form.get("price", type=float)
    stock = request.form.get("stock", type=int) or 0

    if not name or price is None:
        flash("Nome e preco sao obrigatorios.", "danger")
        return redirect(url_for("products.index"))

    image_url = None
    file = request.files.get("image")
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, "..", "uploads", "products")
        os.makedirs(upload_dir, exist_ok=True)
        # Avoid overwriting
        base, ext = os.path.splitext(filename)
        idx = 1
        dest = os.path.join(upload_dir, filename)
        while os.path.exists(dest):
            filename = f"{base}_{idx}{ext}"
            dest = os.path.join(upload_dir, filename)
            idx += 1
        file.save(dest)
        image_url = f"/uploads/products/{filename}"

    product = Product(
        barber_shop_id=current_user.barber_shop_id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
    )
    db.session.add(product)
    db.session.commit()
    flash("Produto criado com sucesso!", "success")
    return redirect(url_for("products.index"))


@products_bp.route("/produtos/<int:id>/editar", methods=["POST"])
@login_required
@tenant_required
def edit(id):
    product = Product.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    product.name = request.form.get("name", "").strip()
    product.description = request.form.get("description", "").strip()
    product.price = request.form.get("price", type=float)
    product.stock = request.form.get("stock", type=int) or 0

    if not product.name or product.price is None:
        flash("Nome e preco sao obrigatorios.", "danger")
        return redirect(url_for("products.index"))

    file = request.files.get("image")
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, "..", "uploads", "products")
        os.makedirs(upload_dir, exist_ok=True)
        dest = os.path.join(upload_dir, filename)
        file.save(dest)
        product.image_url = f"/uploads/products/{filename}"

    db.session.commit()
    flash("Produto atualizado!", "success")
    return redirect(url_for("products.index"))


@products_bp.route("/produtos/<int:id>/excluir", methods=["POST"])
@login_required
@tenant_required
def delete(id):
    product = Product.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()
    db.session.delete(product)
    db.session.commit()
    flash("Produto removido.", "info")
    return redirect(url_for("products.index"))


@products_bp.route("/produtos/<int:id>/toggle-status", methods=["POST"])
@login_required
@tenant_required
def toggle_status(id):
    product = Product.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()
    product.is_active = not product.is_active
    db.session.commit()
    flash("Status do produto atualizado!", "success")
    return redirect(url_for("products.index"))
