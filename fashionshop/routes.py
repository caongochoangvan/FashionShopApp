from flask import redirect, flash, render_template, url_for, request
from fashionshop.forms import RegistrationForm,LoginForm, InforForm, UserForm
from fashionshop import db, bcrypt, app, es
from fashionshop.models import *
from flask_login import current_user, login_user, login_required, logout_user
from product_recommender import *
#TODO: FIX THE SPECIFIC CATEGORIES (MEN, WOMEN, FRAGRANCE, SORT) - paginate

@app.route("/", methods=['GET', 'POST','PUT'])
@app.route("/home")
def home():
    session.permanent = True
    return render_template('home.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form, title = 'Register')
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash(f'Login succesfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Please check the information!','danger')
    return render_template('login.html', form = form, title = 'Login')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    session['firstname'] = request.form.get('firstname')
    session['lastname'] = request.form.get('lastname')
    session['email'] = request.form.get('email')
    session['subject'] = request.form.get('subject')
    session['message'] = request.form.get('message')
    print(session['firstname'], session['lastname'], session['email'], session['subject'],session['message'])
    if session['firstname'] != None:
        flash(f'Message sent!', 'success')
    return render_template('contact.html', tilte = 'Contact')

@app.route('/categories')
def categories():
    page = request.args.get('page', 1, type = int)
    products = Product.query.order_by(Product.title.desc()).paginate(page = page, per_page = 8)
    categories = Category.query.all()
    return render_template('categories.html', title = 'Categories', products = products, categories = categories)
@app.route('/sort', methods = ['POST','GET'])
def soft_products():
    page = request.args.get('page', 1, type = int)
    categories = Category.query.all()
    # products = Product.query.order_by(Product.price.desc()).all()
    sort = int(request.form.get("sort"))
    print(sort)
    sorts = {0 : Product.title, 1: Product.title,2: Product.date_posted, 3: Product.price}       
    products = Product.query.order_by(sorts[sort].desc()).paginate(page = page, per_page = 8)
    return render_template('categories.html', title = 'Categories', products = products, categories = categories)
@app.route('/categories/<string:category_name>')
def category(category_name):
    page = request.args.get('page', 1, type = int)
    categories = Category.query.all()
    category = Category.query.filter_by(name = category_name).first_or_404()
    products = Product.query.filter_by(type = category).paginate(page = page, per_page = 8)
    return render_template('categories.html', title = 'Categories', category = category, products = products, categories = categories)
@app.route('/product/<int:product_id>', methods=['POST','GET'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    comments = Comment.query.filter_by(product = product).order_by(Comment.date_posted.desc())
    print("product", product.title)
    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        if "cart" in session:
            if not any(product.title in d for d in session['cart']):
                session['cart'].append({product.title: quantity})  
            elif any(product.title in d for d in session['cart']):
                # for d in session['cart']:
                #     d.update((k, quantity) for k, v in d.items() if k == product.title)
                for d in session['cart']:
                    d[product.title]+= quantity
        else:
            session['cart'] = [{product.title: quantity}]
        print(session['cart'])
        session['quantity'] = 0
        for k in session['cart']:
            for d in k:
                session['quantity'] += k[d]
   
        flash(f'Adding to shopping cart succesfully!', 'success')
    recommended_index_products = recommender(product_id - 1) 
    print('recommended_index_products', recommended_index_products)
    recommended_products = []
    for id  in recommended_index_products:
        p = Product.query.get(id + 1)
        recommended_products.append(p)
    print('list of recommended products', recommended_products) 
    return render_template('product.html', title = 'Product', product = product, recommended_products = recommended_products, comments = comments)
@app.route('/product/<int:product_id>/new_comment', methods = ['POST','GET'])
@login_required
def new_comment(product_id):
    content = request.args.get('content')
    print(content)
    author = current_user
    product = Product.query.get_or_404(product_id)
    comment = Comment(content = content, author = author, product = product)
    db.session.add(comment)
    db.session.commit()
    flash('Adding new comment successfully!')
    return redirect(url_for('product', product_id = product.id))
@app.route('/checkout', methods=['GET','POST'])
def checkout():
    total = session['total']
    subtotal = session['subtotal']
    shipping = session['shipping']

    form = InforForm()
    if form.validate_on_submit():
        country = request.form.get('country_select')
        infor = Infor(name = form.name.data, address = form.address.data, country = country, city = form.city.data, postcode = form.postcode.data, phone = form.phone.data, total_price = total)
        db.session.add(infor)
        db.session.commit()
        item = []
        if 'order' in session:
            for k in session['order']:
                product = Product.query.filter_by(title = k).first()
                c1 = CartItem(product_id = product.id, quantity = session['order'][k][2])
                item.append(c1)
        infor.cartitems.extend(item)
        db.session.add_all(item)
        db.session.commit()
        flash(f'You ordered successully!', 'success')
        session.pop('cart')
        session.pop('order')
        return redirect(url_for('home'))
    return render_template('checkout.html', title = 'Check Out', form = form, total = total, subtotal = subtotal, shipping = shipping)

@app.route('/cart', methods=['POST','GET'])
def cart():
    # cartitems = []
    # if 'cart' in session:
    #     for d in session['cart']:
    #         for k in d:
    #             # print(type(k), type(d[k]))
    #             product = Product.query.filter_by(title = k).first()
    #             # print(product.type)
    #             cartitem = CartItem(Product = product, quantity = d[k])
    #             # print(cartitem)
    #             # print(cartitem.Product)
    #             cartitems.append(cartitem)
    # print(cartitems) 
    # db.session.add_all(cartitems)  
    # db.session.commit()     
    # print(cartitems[0].Product.title)        
    # print('You have your own items!')
    # subtotal = 0
    # shipping = 10
    # total = subtotal + shipping
    # return render_template('cart.html', title = 'Cart', cartitems = cartitems, total = total, subtotal = subtotal, shipping = shipping)
    subtotal = 0
    order = {}
    session['quantity'] = 0
    if 'cart' in session:
        print(session['cart'])
        for d in session['cart']:
            for k in d:
                # print(type(k), type(d[k]))
                product = Product.query.filter_by(title = k).first()
                # print(product.type)
                # order[product.title] = d[k] 
                order[product.title] = []
                order[product.title].append(product.price) 
                order[product.title].append(product.image_file) 
                order[product.title].append(d[k])
                order[product.title].append(product.price * d[k]) 
                subtotal += product.price * d[k]
                # print(cartitem)
                # print(cartitem.Product) 
                session['quantity'] += d[k]
    
    print(order)   
    session['order'] = order
    print('You have your own items!')
    

    
    shipping = 10
    coupon = 0
    total = subtotal + shipping
    session['shipping'] = shipping
    session['subtotal'] = subtotal
    session['total'] = total

    return render_template('cart.html', title = 'Cart', total = total, subtotal = subtotal, shipping = shipping, order = order)
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    return render_template('cart.html', title = 'Cart')
@app.route('/cart/remove/<string:product_title>', methods=['POST'])
def remove_from_cart(product_title):
    print('before', session['cart'])
    for i in session['cart']:
        if product_title in i:
            i.pop(product_title)
    print('after', session['cart'])
    return redirect(url_for('cart'))
@app.route('/cart/deleteall', methods=['POST'])
def delete_all():
    session.pop('cart')
    return redirect(url_for('cart'))
@app.route('/cart/update',methods=['POST'])
def update_cart():
    # product = Product.query.filter_by(title = p).first()
    qty = request.form.get('update_qty')
    p = request.form.get('update_p')
    print(p,qty)
    print("update_cart")
    
    for i in session['cart']:
        if p in i:
            i.update({p:int(qty)})
    print(session['cart'])
    return redirect(url_for('cart'))
@app.route('/search', methods=['POST','GET'])
def search():
    index_name = 'fashionshop'
    doc_type = 'product'
    query = request.form.get('query')
    print(query)
    # products = Product.query.search(query)
    query = es.search(index = index_name, body={'query':{'match': {'title': query}}})
    found = query['hits']['total']['value']
    products = []
    print(query['hits']['hits'])
    for item in query['hits']['hits']:
        product= Product.query.filter_by(title = item['_source']['title']).first()
        print(product)  
        products.append(product)
    print(products)    
    return render_template('search.html', products = products, found = found)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user', methods = ['GET','POST'])
@login_required
def user():
    form = UserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.birthday = form.birthday.data
        current_user.gender = form.gender.data
        db.session.commit()
        print('Save successfully!')
        flash(f'Your account information has updated!','success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.birthday.data = current_user.birthday
        form.gender.data = current_user.gender
    return render_template('user.html', title='User',  form= form)
    



