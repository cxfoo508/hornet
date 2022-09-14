<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1000px"
    :before-close="closeDialog"
  >
    <el-form
      :model="reportForm"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="统计">
        <div id="myChart" :style="{ width: '380px', height: '380px' }"></div>
      </el-form-item>
      <el-table :data="reportData" border style="width: 100%">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="tests" label="总数" />
        <el-table-column prop="passed" label="通过" />
        <el-table-column prop="error" label="错误" />
        <el-table-column prop="failure" label="失败" />
        <el-table-column prop="skipped" label="跳过" />
        <el-table-column prop="run_time" label="运行时间(S)" />
      </el-table>

      <el-form-item label="详细日志">
        <el-input type="textarea" rows="10" v-model="detailLog" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import ReportsApi from "../../request/reports";

import * as echarts from "echarts";

export default {
  name: "Dialog",
  props: ["rid"],
  components: {},
  data() {
    return {
      showTitle: "查看报告",
      reportData: [],
      dialogVisible: true,
      detailLog: "",
      chartOption: {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: "50%",
            data: [
              { value: 1, name: "跳过" },
              { value: 1, name: "通过" },
              { value: 1, name: "失败" },
              { value: 1, name: "错误" },
            ],
          },
        ],
      },
      reportForm: {
        project: 0,
        name: "",
        describe: "",
        cases: [],
      },
      moduleData: [],
      casesData: [],
      currentModuleId: 0,
      caseNum: 0,
    };
  },
  mounted() {
    //this.initModuleList()
    this.$nextTick(() => {
      this.initChart();
    });
  },
  methods: {
    closeDialog() {
      this.$emit("cancel", {});
    },
    // 初始化图表
    async initChart() {
      var myChart = echarts.init(document.getElementById("myChart"));
      const resp = await ReportsApi.getReportDetail(this.rid);
      this.chartOption.series[0].data = [];
      if (resp.success === true) {
        this.reportData.push(resp.item);
        console.log("resp--->", resp.item);
        this.chartOption.series[0].data.push({
          value: resp.item.skipped,
          name: "跳过",
        });
        this.chartOption.series[0].data.push({
          value: resp.item.passed,
          name: "通过",
        });
        this.chartOption.series[0].data.push({
          value: resp.item.failure,
          name: "失败",
        });
        this.chartOption.series[0].data.push({
          value: resp.item.error,
          name: "错误",
        });
        this.detailLog = resp.item.result;
      }
      myChart.setOption(this.chartOption);
    },
  },
};
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
