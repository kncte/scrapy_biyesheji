
function pollData() {
    const taskType = document.querySelector('#task_type').value;
    $.ajax({
        url: '/get_data?type='+taskType,
        method: 'GET',
        success: function (data) {
            // 在前端处理接收到的数据
            console.log("得到的数据",data)
            updateUI(data);
            if (data['state'] === 'True') {
                // 如果状态为 'stop'，停止轮询
                console.log('Data fetching stopped.');
                return;
            }
            setTimeout(pollData, 2000);
        },
        error: function () {
            // 处理错误
            setTimeout(pollData, 5000); // 设置轮询间隔
        }
    });
}

function updateUI(data) {
    // 在前端更新UI以显示接收到的数据
    var dataList = document.getElementById('data-list');
    dataList.innerHTML = ''; // 清除旧数据

    if (!data.data || !Array.isArray(data.data)) {
        console.error('Invalid data format:', data);
        return;
    }
    var items = data.data.reverse();

    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        // if (item.title && item.rating && item.country) {
        if (item) {
            var listItem = document.createElement('li');
            // var title = item.title;
            // var rating = item.rating;
            // var country = item.country;
            // listItem.textContent = 'Title: ' + title + ', Rating: ' + rating + ', Country: ' + country;
            listItem.textContent = JSON.stringify(item);
            dataList.appendChild(listItem);

             var emptyItem = document.createElement('li');
            emptyItem.textContent = '';  // 设置为空字符串
            dataList.appendChild(emptyItem);
        } else if (item.num) {
            // 处理正在写入数据的信息
            var listItem = document.createElement('li');
            listItem.textContent = item.num;
            dataList.appendChild(listItem);
        }
    }
}

$(document).ready(function () {
    // 绑定表单提交事件
    $('#task-form').submit(function (event) {
        event.preventDefault(); // 阻止默认表单提交行为

        setTimeout(function () {
            pollData();
        }, 5000);
    });
});

