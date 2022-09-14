<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="520px"
    :before-close="closeDiglog"
  >
    <el-form
      :model="moduleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目" prop="name">
        <el-input v-model="proLabel" disabled />
      </el-form-item>
      <el-form-item label="父节点" v-if="parentObj.label !== ''">
        <el-input v-model="parentObj.label" disabled />
      </el-form-item>
      <el-form-item label="模块名" prop="desc">
        <el-input v-model="moduleForm.name" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button type="primary" @click="submitForm('ruleForm')"
          >确 定</el-button
        >
        <el-button @click="closeDiglog">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import ModuleApi from "../../request/module";
export default {
  props: ["rootId", "pid", "proLabel", "parentObj"],
  name: "projectDialog",
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      moduleForm: {
        name: "",
        project_id: 0,
        parent_id: 0,
      },
      rules: {
        name: [{ required: true, message: "请输入模块名称", trigger: "blur" }],
      },
      fileList: [],
    };
  },
  mounted() {
    this.moduleForm.project_id = this.pid;
    if (this.rootId === true) {
      this.showTitle = "创建根节点";
    } else {
      this.showTitle = "创建子节点";
      this.moduleForm.parent_id = this.parentObj.id;
    }
  },
  methods: {
    closeDiglog() {
      this.$emit("cancel", {});
    },

    // 创建节点
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          ModuleApi.createModules(this.moduleForm).then((resp) => {
            if (resp.success === true) {
              this.closeDiglog();
              this.$message.success("创建成功！");
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        }
      });
    },
  },
};
</script>
