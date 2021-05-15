
var database = new Vue({
    el: "#database",
    data: {
        databaseList: ['bangumi_list', 'bilibili', 'acfun', 'AGE', 'others'],
        bilibili: [[20321, '入间同学入魔了 第二季', 'https://www.bilibili.com/bangumi/play/ss38224', '第1话', '2021-05-15'],
            [1300169, '通灵王', 'https://www.bilibili.com/bangumi/play/ss38353', '第7话', '2021-05-13'],
            [5460984, '关于我转生变成史莱姆这档事 转生史莱姆日记', 'https://www.bilibili.com/bangumi/play/ss38221', '第3话', '2021-05-09']],
        bilibiliKeys:['bangumi_id', 'title', 'play_url', 'episode', 'last_update'],
        modifyTemp: {},
        modifyDisplayFlag: false
    },
    methods: {
        deleteItem: function (index) {
            this.bilibili.splice(index, 1)
        },
        modifyItem: function (index, item) {
            this.modifyTemp = {};
            console.log(item);
            for (var x = 0; x < item.length; x++){
                this.$set(this.modifyTemp, this.bilibiliKeys[x], item[x]);
            }
            console.log(this.modifyTemp);
            console.log(this.modifyTemp['bangumi_id']);
            this.modifyDisplayFlag = true;
        }
    }
})

