// 添加验证用户名和邮箱的函数
function validateUser() {
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/validate_user", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.valid) {
                    // 用户名和邮箱匹配，执行下一步操作
                    sendVerificationCode();
                } else {
                    // 用户名和邮箱不匹配，显示错误消息
                    alert(response.message);
                }
            } else {
                // 请求失败的处理
                console.log("请求失败");
            }
        }
    };

    var data = JSON.stringify({
        'username': username,
        'email': email
    });

    xhr.send(data);
}


function resetPassword() {
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var newPassword = document.getElementById('newPassword').value;
    var code = document.getElementById('verificationCode').value;

    // 实现密码重置的逻辑，可以使用 AJAX 请求发送到后端
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/change_pwd", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    // 密码重置成功，等待一秒后执行页面跳转
                    console.log("密码重置成功");
                    alert("密码重置成功");

                    setTimeout(function () {
                        window.location.href = "/login";  // 跳转到登录页面
                    }, 1000);  // 延迟一秒
                } else {
                    // 密码重置失败，显示错误消息
                    console.log("密码重置失败: " + response.message);
                    alert("密码重置失败: " + response.message);
                }
            } else {
                // 请求失败的处理
                console.log("密码重置请求失败");
                alert("密码重置请求失败");
            }
        }
    };

    var data = JSON.stringify({
        'username': username,
        'email': email,
        'new_password': newPassword,
        'code': code
    });

    xhr.send(data);
}


function sendVerificationCode() {
    var email = document.getElementById('email').value;

    // 检查邮箱是否为空
    if (!email) {
        alert('邮箱地址不能为空');
        return;
    }

    // 发送验证码请求
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/send_forget?email=" + email, true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                // 请求成功，可以执行一些操作
                console.log("验证码已发送");
                alert("验证码已发送");
            } else {
                // 请求失败的处理
                console.log("验证码发送失败");
                alert("验证码发送失败: " + xhr.responseText);
            }
        }
    };

    xhr.send();

}
