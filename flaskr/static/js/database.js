var databaseApp;

axios.get("http://106.15.77.207/yukiyu/database").then(initVue(response));

function initVue(_initData) {
    _initData = response.data;
    databaseApp = new Vue({
        el: "#database",
        data: {
            databaseList: _initData['tableList'],
            // 存放数据表的表头
            tableHeaders: {
                bangumi_list: _initData['bangumi_listHeader'],
            },
            // 存放数据表的数据
            tables: {               
                bangumi_list: _initData['bangumi_list'],
            },
            bilibili: [[20321, '入间同学入魔了 第二季', 'https://www.bilibili.com/bangumi/play/ss38224', '第1话', '2021-05-15'],
            [1300169, '通灵王', 'https://www.bilibili.com/bangumi/play/ss38353', '第7话', '2021-05-13'],
            [5460984, '关于我转生变成史莱姆这档事 转生史莱姆日记', 'https://www.bilibili.com/bangumi/play/ss38221', '第3话', '2021-05-09']],
            bilibiliKeys: ['bangumi_id', 'title', 'play_url', 'episode', 'last_update'],
            databaseIndex: 0,
            modifyTemp: {},
            modifyIndex: 0,
            modifyDisplayFlag: false
        },
        methods: {

            changeDatabaseIndex: function (index) {
                var tableName = databaseList[index];
                if (!(tableName in tables)) {
                    var _this = this;
                    axios.get("http://106.15.77.207/yukiyu/database/" + tableName)
                        .then((response) => {
                            data = response.data;
                            _this.tableHeaders[tableName] = data[tableName + 'Header'];
                            _this.table[tableName] = data[tableName];
                            this.databaseIndex = index;
                        })
                }
                this.databaseIndex = index;
            },



            // database CURD part
            deleteItem: function (index) {
                this.bilibili.splice(index, 1)
            },
            modifyItem: function (index, item) {
                this.modifyTemp = {};
                // console.log(item);
                for (var x = 0; x < item.length; x++) {
                    this.$set(this.modifyTemp, this.bilibiliKeys[x], item[x]);
                    // this.modifyTemp.$set(this.bilibiliKeys[x], item[x]);
                }
                // console.log(this.modifyTemp);
                // console.log(this.modifyTemp['bangumi_id']);
                this.modifyIndex = index;
                this.modifyDisplayFlag = true;
            },
            addItem: function () {
                this.modifyItem(this.bilibili.length, Array(this.bilibiliKeys.length).fill(""));
            },
            submitModify: function () {
                var newInfo = [];
                var oldInfo = this.bilibili[this.modifyIndex];
                for (var i = 0; i < this.bilibiliKeys.length; i++) {
                    var temp = this.modifyTemp[this.bilibiliKeys[i]];
                    newInfo.push(temp);
                    // this.bilibili[this.modifyIndex][i] = temp;
                }
                this.submitChanges(oldInfo, newInfo);
                this.$set(this.bilibili, this.modifyIndex, newInfo);
                this.closeModifyPage();
            },
            submitChanges: function (oldInfo, newInfo) {

            },
            closeModifyPage: function () {
                this.modifyDisplayFlag = false;
            }
            // end database CURD part 
        }
    })
}


