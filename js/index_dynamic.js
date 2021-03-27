// we use this script to access api
var now = new Date();

var weekChoose = new Vue({
    el: "#week-choose",
    data: {
        weeks: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        mark: (now.getDay() + 6) % 7
    },
    methods: {
        choose: function (index) {
            this.mark = index
        }
    }
})


var bangumiList = new Vue({
    el: "#bangumi-list",
    data: {
        showMark:-1,
        // bangumiGet:axios.get("http://106.15.77.207/bangumi")
        bangumiGet:[{'name':'五等分的新娘', 'play_url': {'bili': 'https://www.bilibili.com/bangumi/play/ss36166/?spm_id_from=333.851.b_62696c695f7265706f72745f616e696d65.34', '樱花':'#'},
        'episode': '第12话', 'img': 'https://i0.hdslb.com/bfs/bangumi/image/dda6999ee8867f8496f914461f4d175a664429fe.png@70w_70h_1c_100q.webp'}]
    },
    methods: {
        getPlayUrl: function (index) {
            var urlList = this.bangumiGet[index]['play_url'];
            var firstKey = Object.keys(urlList)[0];
            return urlList[firstKey];
        },
        showUrlList: function (index) {
            this.showMark = index;
        },
        hideUrlList: function () {
            this.showMark = -1;
        }
    }
})