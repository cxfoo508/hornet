<template>
  <div class="tasks">
    <div style="height: 100px; width: 100%">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="项目列表" style="float: left">
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
        <el-form-item style="float: right">
          <el-button type="primary" @click="createTasks()" size="medium"
            >创建任务</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-table :data="tasksData" border style="width: 100%">
        <el-table-column fixed prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="名称" width="220" />
        <el-table-column prop="describe" label="描述" width="400" />
        <el-table-column prop="create_time" label="创建时间" width="250" />
        <el-table-column prop="update_time" label="更新时间" width="250" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <div v-if="scope.row.status === 0">
              <el-tag type="info">未执行</el-tag>
            </div>
            <div v-else-if="scope.row.status === 1">
              <el-tag type="success">执行中</el-tag>
            </div>
            <div v-else-if="scope.row.status === 2">
              <el-tag>已执行</el-tag>
            </div>
            <div v-else>
              <el-tag type="danger">未知状态</el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" width="250">
          <template slot-scope="scope">
            <el-button
              @click="runningTasks(scope.row)"
              type="text"
              size="medium"
              >执行</el-button
            >
            <el-button @click="editTasks(scope.row)" type="text" size="small"
              >编辑</el-button
            >
            <el-button @click="deleteTasks(scope.row)" type="text" size="small"
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
    <tasksDialog
      v-if="dialogFlag"
      @cancel="closeDiglog"
      :title="dialogTitle"
      :pid="projectTaskId"
      :tid="taskId"
    />
  </div>
</template>

<script>
// @ is an alias to /src
import ProjectApi from "../../request/project";
import TasksApi from "../../request/tasks";
import tasksDialog from "./tasksDialog";

export default {
  name: "tasks",
  components: {
    tasksDialog,
  },
  data() {
    return {
      tasksReq: {
        project_id: 1,
        page: 1,
        size: 6,
      },
      projectTaskId: 1,
      projectTaskOptions: [],
      total: 50,
      dialogFlag: false,
      dialogTitle: "create",
      tasksData: [],
      taskId: "",
      taskHeartbeat: null,
    };
  },
  mounted() {
    this.initProjectlist();
    this.taskHeartbeat = setInterval(() => {
      this.initTasksList();
    }, 5000);
  },
  destroyed() {
    clearInterval(this.taskHeartbeat);
  },

  methods: {
    deleteTask(index, rows) {
      rows.splice(index, 1);
    },

    onSubmit() {
      console.log("submit!");
    },

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
        this.initTasksList();
      }
    },
    //初始化任务列表
    async initTasksList() {
      this.tasksReq.project_id = this.projectTaskId;
      const resp = await TasksApi.getTasksList(this.tasksReq);
      if (resp.success === true) {
        this.total = resp.total;
        console.log("total__>", resp);
        this.tasksData = resp.items;
      }
    },
    //修改选中的项目
    changeProject(value) {
      this.projectTaskId = value;
      this.initTasksList();
    },
    //删除任务
    async deleteTasks(row) {
      const resp = await TasksApi.deleteTask(row.id);
      if (resp.success === true) {
        this.$message.success("删除成功");
        this.initProjectlist();
      } else {
        this.$message.error("删除失败");
      }
    },
    //执行任务
    async runningTasks(row) {
      const resp = await TasksApi.runTasks(row.id);
      if (resp.success === true) {
        this.$message.success("执行成功");
        //this.initProjectlist();
      } else {
        this.$message.error("执行失败");
      }
    },
    //创建任务
    createTasks() {
      this.dialogTitle = "create";
      this.dialogFlag = true;
    },
    //编辑任务
    editTasks(row) {
      this.dialogTitle = "edit";
      this.taskId = row.id;
      console.log("taskid-->", this.taskId);
      this.dialogFlag = true;
    },
    //关闭弹窗
    closeDiglog() {
      this.dialogFlag = false;
      this.initTasksList();
    },
    //跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.tasksReq.page = val;
      this.initTasksList();
    },
  },
};
</script>
<style>
.box-card {
}
</style>
