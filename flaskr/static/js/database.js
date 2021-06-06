var databaseApp;

axios.get("http://106.15.77.207/yukiyu/database?name1=tables&name2=bangumi_list").then(initVue);

function initVue(_initData) {
    _initData = _initData.data;
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
                var tableName = this.databaseList[index];
                var _this = this;
                axios.get("http://106.15.77.207/yukiyu/database?name=" + tableName)
                    .then((response) => {
                        data = response.data;
                        _this.$set(_this.tableHeaders, tableName, data[tableName + 'Header']);
                        _this.$set(_this.tables, tableName, data[tableName]);
                        // _this.tableHeaders[tableName] = data[tableName + 'Header'];
                        // _this.tables[tableName] = data[tableName];
                        this.databaseIndex = index;
                    })
            },



            // database CURD part
            deleteItem: function (index) {
                // this.bilibili.splice(index, 1)
                var targetDatabase = this.databaseList[this.databaseIndex];
                // console.log(targetDatabase);
                // console.log(index);
                var deleteTarget = this.tables[targetDatabase].splice(index, 1)[0];
                // console.log('delete item:')
                // console.log(deleteTarget)
                this.submitChanges(deleteTarget, null, targetDatabase)
            },
            modifyItem: function (index, item) {
                this.modifyTemp = {};
                var targetDatabase = this.databaseList[this.databaseIndex];
                // console.log(item);
                for (var x = 0; x < item.length; x++) {
                    this.$set(this.modifyTemp, this.tableHeaders[targetDatabase][x], item[x]);
                    // this.$set(this.modifyTemp, this.bilibiliKeys[x], item[x]);
                    // this.modifyTemp.$set(this.bilibiliKeys[x], item[x]);
                }
                // console.log('modify temp below:');
                // console.log(this.modifyTemp);
                // console.log(this.modifyTemp['bangumi_id']);
                this.modifyIndex = index;
                this.modifyDisplayFlag = true;
            },
            addItem: function () {
                var targetDatabase = this.databaseList[this.databaseIndex];
                this.modifyItem(this.tables[targetDatabase].length, Array(this.tableHeaders[targetDatabase].length).fill(""));
                // this.modifyItem(this.bilibili.length, Array(this.bilibiliKeys.length).fill(""));
            },
            submitModify: function () {
                var targetDatabase = this.databaseList[this.databaseIndex];
                var newInfo = [];
                var oldInfo = null;
                if (this.tables[targetDatabase].length != this.modifyIndex) {
                    oldInfo = this.tables[targetDatabase][this.modifyIndex];
                }
                // var oldInfo = this.bilibili[this.modifyIndex];
                // for (var i = 0; i < oldInfo.length; i++) {
                //     var temp = this.modifyTemp[this.bilibiliKeys[i]];
                //     newInfo.push(temp);
                //     // this.bilibili[this.modifyIndex][i] = temp;
                // }
                for (key in this.modifyTemp) {
                    newInfo.push(this.modifyTemp[key]);
                }
                this.submitChanges(oldInfo, newInfo, targetDatabase);
                // console.log('set temp into target');
                // console.log('new info:');
                // console.log(newInfo);
                this.$set(this.tables[targetDatabase], this.modifyIndex, newInfo);
                this.closeModifyPage();
            },
            submitChanges: function (oldInfo, newInfo, tableName) {
                var config = {
                    tableName: tableName,
                    oldInfo: oldInfo,
                    newInfo: newInfo
                }
                axios.post("http://106.15.77.207/yukiyu/database", config)
                    .then((response) => {
                        console.log(response);
                        var returnStatu = response.data
                        if (returnStatu.statu != 1) {
                            alert(returnStatu.info)
                        }
                    })
                    .catch((response) => {
                        console.log(response);
                    })
            },
            closeModifyPage: function () {
                this.modifyDisplayFlag = false;
            }
            // end database CURD part 
        }
    })
}


