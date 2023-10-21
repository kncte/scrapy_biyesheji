document.addEventListener("DOMContentLoaded", function () {
    // 公共元素
    let navigation = document.querySelector('.navigation');
    let menuToggle = document.querySelector('.menuToggle');
    let con2 = document.querySelector('.layui-body');

    // 菜单切换
    menuToggle.addEventListener('click', function () {
        navigation.classList.toggle('active');
        const a1 = navigation.getBoundingClientRect();
        const a2 = con2.getBoundingClientRect();
        con2.style.marginLeft = (a1.right < 270) ? '100px' : '0px';
        con2.style.transition = '0.5s';
    });


    // 用户信息更新
    fetch('/get_user')
        .then(response => {
            console.log("zzzz", response)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {

            if (data) {
                // 延迟一段时间再执行更新操作
                updateUserInfo(data);

            } else {
                console.error('Failed to fetch user information');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });


    function updateUserInfo(data) {
        console.log('Updating user info:', data);
        const userAvatar = document.getElementById('user-avatar');
        const users = document.getElementById('users');
        const username_p1 = document.getElementById('p1');
        const nickname_p3 = document.getElementById('p3');
        const email_p2 = document.getElementById('p2');
        const user_name = document.getElementById('user-name');

        // 获取用户信息后

        user_name.textContent = data.username;
        // 更新头像地址
        userAvatar.src = data.avatarUrl;
        users.textContent = (data.IsAdmin === 1) ? "管理员" : "用户";
        username_p1.textContent = "当前用户名: " + data.username;
        nickname_p3.textContent = "当前昵称: " + data.nickname;
        email_p2.textContent = "当前邮箱: " + data.email;
    }

    // 安全设置弹出窗口
    const securityLink = document.querySelector('#security-link');
    const securityOverlay = document.querySelector('#security-overlay');
    const updatePasswordBtn = document.querySelector('#update-password-btn');

    securityLink.addEventListener('click', function () {
        securityOverlay.style.display = 'flex';
    });

    updatePasswordBtn.addEventListener('click', function () {
        // ...（你的密码更新逻辑）
        var formData1 = new FormData();
        formData1.append('oldpassword', oldpassword_input.value);
        formData1.append('newpassword', newpassword_input.value);
        fetch('/change_password', {
            method: 'POST',
            body: formData1
        })
            .then(response => response.json())
            .then(data => {
                if (data.code === 0) {
                    console.log("修改成功")
                } else {
                    console.log('Update failed:', data.message);
                    console.error('Update failed:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        securityOverlay.style.display = 'none';
    });

    // layui元素模块
    layui.use('element', function () {
        var $ = layui.jquery,
            element = layui.element;

        var active = {
            tabAdd: function () {
                // ...（你的tab添加逻辑）

                var htmlurl = $(this).attr('data-url');
                var mytitle = $(this).attr('mytitle');
                console.log(htmlurl, mytitle)
                var arrayObj = [];　//创建一个数组
                $(".layui-tab-title").find('li').each(function () {
                    var y = $(this).attr("lay-id");
                    arrayObj.push(y);
                });
                var have = $.inArray(mytitle, arrayObj);  //返回 3,
                if (have >= 0) {

                    element.tabChange('demo', mytitle); //切换到当前点击的页面
                } else {

                    element.tabAdd('demo', {
                        title: mytitle //用于演示
                        ,
                        content: '<iframe style="width: 95%;height: 100vh;" scrolling="auto" src="' + htmlurl + '"></iframe>'
                        ,
                        id: mytitle //实际使用一般是规定好的id，这里以时间戳模拟下
                    })
                    var iframe = document.querySelector('iframe[src="' + htmlurl + '"]');
                    iframe.addEventListener('load', function () {
                        var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                        var innerHeight = innerDoc.body.scrollHeight - 5;
                        iframe.style.height = innerHeight + 'px';
                    });
                    element.tabChange('demo', mytitle); //切换到当前点击的页面
                }
            }
        };

        // $(".leftdaohang").click(function () {
        //     var type = "tabAdd";
        //     var othis = $(this);
        //     active[type] ? active[type].call(this, othis) : '';
        // });

                $(".leftdaohang").click(function () {
                console.log("点击事件触发了");

                // 移除所有 li 的 active 类
                $(".leftdaohang").removeClass("active");

                // 给当前点击的 li 添加 active 类
                $(this).addClass("active");

                var type = "tabAdd";
                var othis = $(this);
                active[type] ? active[type].call(this, othis) : '';
            });
    });

    // 个人信息部分...

    var basicInfoLink = document.getElementById('basic-info-link');
    var avatarModal = document.getElementById('avatar-modal');
    var closeBtn = document.querySelector('.modal-content .close');

    basicInfoLink.addEventListener('click', function () {

        avatarModal.style.display = 'block';
        modalAvatar.src = userAvatar.src;
    });

    closeBtn.addEventListener('click', function () {
        avatarModal.style.display = 'none';
    });

    var saveChangesBtn = document.getElementById('save-changes-btn');
    var usernameInput = document.getElementById('username-input');
    var emailInput = document.getElementById('email-input');
    var nicknameInput = document.getElementById('nickname-input');
    var p1Elements = document.getElementById('p1');
    var p2Elements = document.getElementById('p2');
    var p3Elements = document.getElementById('p3');
    var p1 = p1Elements[0];
    var p2 = p2Elements[0];
    var p3 = p3Elements[0];

    saveChangesBtn.addEventListener('click', function () {
        var formData = new FormData();
        formData.append('avatar', fileInput.files[0]);
        formData.append('username', usernameInput.value);
        formData.append('email', emailInput.value);
        formData.append('nickname', nicknameInput.value);

        fetch('/update_profile', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.code === 0) {

                    userAvatar.src = modalAvatar.src; // Update user avatar
                    if (usernameInput.value !== "") {
                        p1Elements.textContent = "当前用户名: " + usernameInput.value;
                    }
                    if (emailInput.value !== "") {
                        p2Elements.textContent = "当前邮箱: " + emailInput.value;
                    }
                    if (nicknameInput.value !== "") {
                        p3Elements.textContent = "当前昵称: " + nicknameInput.value;
                    }
                    avatarModal.style.display = 'none'; // Close the modal
                } else {
                    console.error('Update failed:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });


        // $(".leftdaohang").click(function () {
        //     console.log("点击事件触发了");
        //
        //     // 移除所有 li 的 active 类
        //     $(".leftdaohang").removeClass("active");
        //
        //     // 给当前点击的 li 添加 active 类
        //     $(this).addClass("active");
        //
        //     var type = "tabAdd";
        //     var othis = $(this);
        //     active[type] ? active[type].call(this, othis) : '';
        // });


    var userAvatar = document.getElementById('user-avatar');
    var modalAvatar = document.getElementById('modal-avatar');
    var closeModalBtn = document.getElementsByClassName('close')[0];
    var closeModalBtn222 = document.getElementsByClassName('close1')[0];
    var changeAvatarBtn = document.getElementById('change-avatar-btn');
    var fileInput = document.getElementById('file-input');

    // const securityOverlay = document.querySelector('#security-overlay');
    userAvatar.addEventListener('click', function () {
        avatarModal.style.display = 'block';
        modalAvatar.src = userAvatar.src;
    });

    closeModalBtn.addEventListener('click', function () {
        avatarModal.style.display = 'none';
    });

    closeModalBtn222.addEventListener('click', function () {
        securityOverlay.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === avatarModal) {
            avatarModal.style.display = 'none';
        }
    });

    changeAvatarBtn.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        var selectedFile = fileInput.files[0];
        if (selectedFile) {
            modalAvatar.src = URL.createObjectURL(selectedFile);
            avatarModal.style.display = 'block';
        }
    });
});
