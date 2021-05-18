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
                bangumiGet:response.data.result,
                showDetailFlag: false,
                bangumiDetail: {
                    // name,company_name,conduct_name,img
                    name: '这爱情有点奇怪',
                    img: '../static/upload/default.webp',
                    company_name: 'company company company',
                    conduct_name: 'conduct',
                    cast:['aaaa', 'bbbb', 'cccc', 'dddd', 'eeeeeee', 'fff', 'ggggggggggggg', 'hhh']
                }
            },
            methods: {
                getPlayUrl: function (item, index) {
                    var urlList = item.play_url;
                    var firstKey = Object.keys(urlList)[0];
                    return urlList[firstKey];
                    // return urlList;
                },
                changeWeekMark: function (index) {
                    this.weekMark = index;
                },
                showUrlList: function (index) {
                    this.showMark = index;
                },
                hideUrlList: function () {
                    this.showMark = -1;
                },

                getDetailInfo: function(item){
                    var id = item.bangumi_id;
                    axios.get("http://106.15.77.207/bangumi?id="+id)
                        .then((response) => {
                            this.bangumiDetail = response.data.result;
                            console.log('get info from server:');
                            console.log(this.bangumiDetail);
                            this.showDetailFlag = true
                        })
                }
            }
        })
    })
