from flask import Flask, json, redirect, render_template, request, jsonify, url_for
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "ho394jkfkfhgsgg"
jwt = JWTManager(app)
revoked_tokens = set()
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        access_token = create_access_token(
        identity=username, 
        additional_claims={"role": role}  
         )
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Sai tài khoản hoặc mật khẩu"}), 401

# API lấy thông tin user (cần token)
@app.route('/check_token', methods=["GET"])
@jwt_required()
def check_token():
    username = get_jwt_identity()  # Lấy username từ identity
    claims = get_jwt()  # Lấy toàn bộ claims
    role = claims["role"]  # Lấy role từ claims
    if role == "admin":
        return render_template("admin.html")
    elif role == "user":
        return render_template("user.html")
    else:
        return render_template("index.html")
@app.route('/admin', methods=["GET"])
@jwt_required()
def admin():
    return jsonify("dang nhap thanh cong")
@app.route('/user', methods=["GET"])
@jwt_required()
def user():
    return jsonify("dang nhap thanh cong")

@app.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"] 
    revoked_tokens.add(jti)
    return jsonify({"msg": "Đăng xuất thành công"}), 200
if __name__ == "__main__":
    app.run(debug=True)
