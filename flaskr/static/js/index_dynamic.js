var now = new Date();

// var weekChoose = new Vue({
//     el: "#week-choose",
//     data: {
//         weeks: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
//         mark: (now.getDay() + 6) % 7
//     },
//     methods: {
//         chooseForHD: function (index) {
//             console.log("hd mark changed")
//             this.mark = index;
//         }
//     }
// })

axios.get("http://106.15.77.207/bangumi")
    .then(function (response) {
        console.log(response)
        var bangumiList = new Vue({
            el: "#bangumi",
            data: {
                showMark: -1,
                weeks: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                weekMark: (now.getDay() + 6) % 7,
                bangumiGet:response.data.result
                // bangumiGet:[{'name':'五等分的新娘', 'play_url': {'bili': 'https://www.bilibili.com/bangumi/play/ss36166/?spm_id_from=333.851.b_62696c695f7265706f72745f616e696d65.34', '樱花':'#'},
                // 'episode': '第12话', 'img': '../static/upload/五等分.webp'}]
            },
            methods: {
                getPlayUrl: function (item, index) {
                    var urlList = item.play_url;
                    // var firstKey = Object.keys(urlList)[0];
                    // return urlList[firstKey];
                    return urlList;
                },
                changeWeekMark: function (index) {
                    this.weekMark = index;
                },
                showUrlList: function (index) {
                    this.showMark = index;
                },
                hideUrlList: function () {
                    this.showMark = -1;
                }
            }
        })
    })
