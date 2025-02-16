from flask import Flask, json, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/index_admin')
def index_admin():
    return render_template("admin.html")
# API đăng nhập
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        access_token = create_access_token(
        identity=username,  # Chỉ truyền username vào identity
        additional_claims={"role": role}  # Lưu role vào claims
         )
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Sai tài khoản hoặc mật khẩu"}), 401

# API lấy thông tin user (cần token)
@app.route("/check_token", methods=["GET"])
@jwt_required()
def check_token():
    username = get_jwt_identity()  # Lấy username từ identity
    claims = get_jwt()  # Lấy toàn bộ claims
    role = claims["role"]  # Lấy role từ claims
    if role == "admin":
        return jsonify({"redirect": "./admin.html"})
    elif role == "user":
        return jsonify({"redirect": "/user.html"})

@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()  # Lấy toàn bộ claims
    role = claims["role"]  # Lấy role từ claims
    if role != "admin":
        return jsonify({"msg": "Bạn không có quyền truy cập!"}), 403
    return jsonify({"msg": "Chào mừng Admin!"})

if __name__ == "__main__":
    app.run(debug=True)
