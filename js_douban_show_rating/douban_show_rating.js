// ==UserScript==
// @name         豆瓣电影显示TMDB和IMDb评分和链接
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  在豆瓣电影页面显示对应的TMDB和IMDb条目评分和链接
// @author       You
// @match        https://movie.douban.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
      // 获取要隐藏的元素
    const ratingBetterthanElement = document.querySelector('.rating_betterthan');

    // 隐藏元素
    if (ratingBetterthanElement) {
        ratingBetterthanElement.style.display = 'none';
    }

    // 创建一个容器元素
    const ratingsContainer = document.createElement('div');
    ratingsContainer.style.display = 'flex'; // 使用 Flexbox 布局
    ratingsContainer.style.alignItems = 'center'; // 垂直居中对齐（可选）
    ratingsContainer.style.gap = '35px'; // 添加间距，这里设置为10像素，你可以根据需要调整

    // 获取豆瓣电影页面的电影名称
    const movieName = document.querySelector('span[property="v:itemreviewed"]').textContent.trim();

    // 获取 IMDb 条目 ID
    const imdbIdElement = document.body.innerHTML.match(/<span class="pl">IMDb:<\/span>\s*(.*?)<br>/);
    const imdbId = imdbIdElement ? imdbIdElement[1] : null;


    console.log('IMDb ID:', imdbId); // Debug output

    // 构建TMDB搜索API的URL
    const tmdbSearchUrl = `https://api.themoviedb.org/3/search/movie?api_key=YOUR_TMDB_API_KEY&query=${encodeURIComponent(movieName)}`;

    // 发送请求获取TMDB搜索结果
fetch(tmdbSearchUrl)
    .then(response => response.json())
    .then(data => {
        // 获取第一个搜索结果（最相关的电影）
        const tmdbMovie = data.results[0];

        if (tmdbMovie) {
            // 格式化TMDB评分为一位小数
            const formattedTmdbRating = tmdbMovie.vote_average.toFixed(1);

            // 创建显示TMDB评分和链接的元素
            const tmdbRatingElement = document.createElement('div');
            tmdbRatingElement.innerHTML = `<div class="rating_self clearfix">TMDB<br/><a href="https://www.themoviedb.org/movie/${tmdbMovie.id}" target="_blank"><strong class="ll rating_num" property="v:average">${formattedTmdbRating}</strong></a></div>`;

            // 如果有 IMDb ID，获取 IMDb 评分并显示
            if (imdbId) {
                const imdbRatingUrl = `https://www.omdbapi.com/?apikey=YOUR-OMDB-API-KEY&i=${imdbId}`;
                fetch(imdbRatingUrl)
                    .then(response => response.json())
                    .then(imdbData => {
                        const imdbRating = imdbData.imdbRating;

                        console.log('IMDb Rating:', imdbRating); // Debug output

                        // 创建显示 IMDb 评分和链接的元素
                        const imdbRatingElement = document.createElement('div');
                        imdbRatingElement.innerHTML = `<div class="rating_self clearfix">IMDb<br/><a href="https://www.imdb.com/title/${imdbId}" target="_blank"><strong class="ll rating_num" property="v:average">${imdbRating}</strong></a></div>`;

                        // 将 IMDb 元素插入到容器
                        ratingsContainer.appendChild(imdbRatingElement);
                    })
                    .catch(error => {
                        console.error('Error fetching IMDb data:', error);
                    });
            }

            // 将 TMDB 元素插入到容器
            ratingsContainer.appendChild(tmdbRatingElement);

            // 将容器插入到豆瓣电影页面中
            const ratingBetterthanElement = document.querySelector('.rating_betterthan');
            ratingBetterthanElement.parentNode.insertBefore(ratingsContainer, ratingBetterthanElement.nextSibling);
        }
    })
    .catch(error => {
        console.error('Error fetching TMDB data:', error);
    });
})();
