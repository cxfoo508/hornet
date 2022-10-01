<template>
  <div class="tasks">
    <div style="height: 100px; text-align: left; width: 100%">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="项目列表">
          <el-select
            v-model="projectTaskId"
            placeholder="请选择项目"
            @change="changeProject"
          >
            <el-option
              v-for="item in projectTaskOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-table :data="reportData" border style="width: 100%">
        <el-table-column
          fixed
          prop="id"
          label="ID"
          min-width="5%"
        ></el-table-column
        >>
        <el-table-column
          prop="name"
          label="名称"
          min-width="11%"
        ></el-table-column>
        <el-table-column
          prop="tests"
          label="总数"
          min-width="5%"
        ></el-table-column>
        <el-table-column prop="passed" label="通过" min-width="5%">
          <template slot-scope="scope">
            <el-tag type="success">{{ scope.row.passed }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error" label="错误" min-width="5%">
          <template slot-scope="scope">
            <el-tag type="danger">{{ scope.row.error }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="failure" label="失败" min-width="5%">
          <template slot-scope="scope">
            <el-tag type="Warning">{{ scope.row.failure }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="skipped" label="跳过" min-width="5%">
          <template slot-scope="scope">
            <el-tag type="info">{{ scope.row.skipped }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="run_time"
          label="运行时间"
          min-width="5%"
        ></el-table-column>
        <el-table-column
          prop="create_time"
          label="创建时间"
          min-width="10%"
        ></el-table-column>

        <el-table-column fixed="right" label="操作" width="250">
          <template slot-scope="scope">
            <el-button @click="showReport(scope.row)" type="text" size="small"
              >查看</el-button
            >
            <el-button @click="deleteReport(scope.row)" type="text" size="small"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="text-align: right">
      <el-pagination
        cy-data="ProjectPagination"
        background
        @current-change="handleCurrentChange"
        layout="prev, pager, next"
        :page-size="tasksReq.size"
        :total="total"
      >
      </el-pagination>
    </div>
    <reportDialog v-if="dialogFlag" @cancel="closeDiglog" :rid="reportId" />
  </div>
</template>

<script>
// @ is an alias to /src
import ProjectApi from "../../request/project";
import TasksApi from "../../request/tasks";
import ReportsApi from "../../request/reports";
import reportDialog from "./reportDialog";

export default {
  name: "report",
  components: {
    reportDialog,
  },
  data() {
    return {
      projectTaskId: 1,
      projectTaskOptions: [],
      total: 50,
      dialogFlag: false,
      tasksReq: {
        project_id: 1,
        page: 1,
        size: 6,
      },
      reportData: [],
      reportId: "",
    };
  },
  mounted() {
    this.initProjectlist();
  },
  methods: {
    //初始化项目列表接口
    async initProjectlist() {
      const resp = await ProjectApi.getProjects();
      if (resp.success === true) {
        this.projectTaskId = resp.items[0].id;
        for (let i = 0; i < resp.items.length; i++) {
          this.projectTaskOptions.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          });
        }
        this.initReportList();
      }
    },
    //初始化报告列表
    async initReportList() {
      this.tasksReq.project_id = this.projectTaskId;
      const resp = await ReportsApi.getReportList(this.tasksReq);
      if (resp.success === true) {
        this.total = resp.total;
        this.reportData = resp.items;
      }
    },
    //修改选中的项目
    changeProject(value) {
      this.projectTaskId = value;
      this.initReportList();
    },
    //删除报告
    async deleteTasks(row) {
      const resp = await TasksApi.deleteTask(row.id);
      if (resp.success === true) {
        this.$message.success("删除成功");
        this.initProjectlist();
      } else {
        this.$message.error("删除失败");
      }
    },
    //查看报告
    showReport(row) {
      this.reportId = row.id;
      this.dialogFlag = true;
    },
    //关闭弹窗
    closeDiglog() {
      this.dialogFlag = false;
      this.initReportList();
    },
    //跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.tasksReq.page = val;
      this.initReportList();
    },
  },
};
</script>
<style>
.box-card {
}
</style>
