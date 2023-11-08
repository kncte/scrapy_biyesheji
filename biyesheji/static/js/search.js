
function handleCategoryChange() {
    var categorySelect = document.querySelector(".select_1");
    var selectedValue = categorySelect.value;

    if (selectedValue === "music") {
        searchMusic()
    } else if (selectedValue === "movie") {
        searchMovies()
    } else if (selectedValue === "new") {
        searchNew()
    }
}

function searchNew() {
    var keyword = document.getElementById("keyword").value;
    if (keyword ===''){
        alert("请输入查询的关键字")
        return
    }
    // 发送 Ajax 请求到搜索路由
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `/search_new?keyword=${keyword}`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            NewResults(response);
        }
    };
    xhr.send();
}

function NewResults(results) {
    var resultDiv = document.querySelector(".result-container");
    if (results.length > 0) {
        var table = document.createElement("table");
        // 创建表头
        table.style.tableLayout = "fixed";
        var tableHeader = document.createElement("tr");
        tableHeader.innerHTML = "<th>标题</th><th>大概内容</th><th>新闻链接</th><th>发布时间</th><th>新闻来源</th>";
        table.appendChild(tableHeader);

        // 逐行生成表格数据
        for (var i = 0; i < results.length; i++) {
            var New = results[i];
            var row = document.createElement("tr");
            row.innerHTML = `
                <td class="truncate news-title">${New.title}</td>
                <td class="truncate news-content">${New.content}</td>
                <td class="truncate">${New.urls}</td>
                <td class="truncate">${New.news_time}</td>
                <td class="truncate">${New.from_source}</td>`;
            table.appendChild(row);
        }

        resultDiv.innerHTML = "<h2>搜索结果：</h2>"; // 清空原有内容
        resultDiv.appendChild(table); // 将表格添加到 .result 容器中

        // 为每个单元格添加点击事件
        var cells = document.querySelectorAll('.truncate');
        cells.forEach(function (cell) {
            cell.addEventListener('click', function () {
                showModal(cell.textContent);
            });
        });

    } else {
        resultDiv.innerHTML = "<p>没有找到匹配的新闻。</p>";
    }
    document.body.appendChild(resultDiv);


}


// 其他函数保持不变


function searchMusic() {
    var keyword = document.getElementById("keyword").value;
    if (keyword ===''){
        alert("请输入查询的关键字")
        return
    }
    // 发送 Ajax 请求到搜索路由
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `/search_music?keyword=${keyword}`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            MusicResults(response);
        }
    };
    xhr.send();
}

function searchMovies() {
    var keyword = document.getElementById("keyword").value;
    if (keyword ===''){
        alert("请输入查询的关键字")
        return
    }
    // 发送 Ajax 请求到搜索路由
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `/search_movie?keyword=${keyword}`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            displayResults(response);
        }
    };
    xhr.send();
}

function MusicResults(results) {
    var resultDiv = document.querySelector(".result-container");
    if (results.length > 0) {
        var table = document.createElement("table");
        // 创建表头
        var tableHeader = document.createElement("tr");
        tableHeader.innerHTML = "<th>歌名</th><th>歌手</th><th>专辑名</th><th>MP3地址</th>";
        table.appendChild(tableHeader);

        // 逐行生成表格数据
        for (var i = 0; i < results.length; i++) {
            var music = results[i];
            var row = document.createElement("tr");
            row.innerHTML = `<td class="clickable">${music.music_name}</td>
                            <td class="clickable">${music.singer}</td>
                            <td class="clickable">${music.Album_Name}</td>
                            <td class="clickable">${music.mp3_url}</td>
            `;
            table.appendChild(row);
        }

        resultDiv.innerHTML = "<h2>搜索结果：</h2>"; // 清空原有内容
        resultDiv.appendChild(table); // 将表格添加到 .result 容器中

        // 为每个单元格添加点击事件
        var cells = document.querySelectorAll('.clickable');
        cells.forEach(function (cell) {
            cell.addEventListener('click', function () {
                showModal(cell.textContent);
            });
        });
    } else {
        resultDiv.innerHTML = "<p>没有找到匹配的音乐。</p>";
    }
    document.body.appendChild(resultDiv);
}

function displayResults(results) {
    var resultDiv = document.querySelector(".result-container")
    if (results.length > 0) {
        var table = document.createElement("table");
        // 创建表头
        var tableHeader = document.createElement("tr");
        tableHeader.innerHTML = "<th>电影名</th><th>评分</th><th>国家</th><th>地址</th>";
        table.appendChild(tableHeader);

        // 逐行生成表格数据
        for (var i = 0; i < results.length; i++) {
            var movie = results[i];
            var row = document.createElement("tr");
            row.innerHTML = `<td>${movie.title}</td>
                             <td>${movie.rating}</td>
                             <td>${movie.country}</td>
                             <td>${movie.address}</td>`;
            table.appendChild(row);
        }

        resultDiv.innerHTML = "<h2>搜索结果：</h2>";
        resultDiv.appendChild(table);

        // 为每个单元格添加点击事件
        var cells = document.querySelectorAll('td');
        cells.forEach(function (cell) {
            cell.addEventListener('click', function () {
                showModal(cell.textContent);
            });
        });
    } else {
        resultDiv.innerHTML = "<p>没有找到匹配的电影。</p>";
    }

    document.body.appendChild(resultDiv);
}



    function showModal(content) {
        // 创建模态框
        var modal = document.createElement('div');
        modal.className = 'modal';

        // 创建关闭按钮
        var closeBtn = document.createElement('span');
        closeBtn.className = 'close';
        closeBtn.innerHTML = '&times;';

        // 为关闭按钮添加点击事件
        closeBtn.addEventListener('click', function () {
            closeModal();
        });

        // 将关闭按钮添加到模态框中
        modal.appendChild(closeBtn);

        // 创建模态框内容
        var modalContent = document.createElement('div');
        modalContent.className = 'modal-content';

        // 将内容添加到模态框中
        modalContent.textContent = content;
        modal.appendChild(modalContent);

        // 将模态框添加到 body 中
        document.body.appendChild(modal);

        // 显示模态框
        modal.style.display = 'flex';

        // 添加点击事件监听器，点击模态框外部关闭模态框
        window.addEventListener('click', function (event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }

    function closeModal() {
        // 隐藏模态框
        var modal = document.querySelector('.modal');
        modal.style.display = 'none';

        // 移除模态框
        document.body.removeChild(modal);
    }