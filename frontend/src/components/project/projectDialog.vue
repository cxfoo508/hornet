<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="520px"
    :before-close="closeDiglog"
  >
    <el-form
      :model="projectForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目名称" prop="name">
        <el-input v-model="projectForm.name" />
      </el-form-item>
      <el-form-item label="项目描述" prop="desc">
        <el-input type="textarea" v-model="projectForm.describe" />
      </el-form-item>
      <el-form-item label="上传图片" prop="desc">
        <el-upload
          action="#"
          :before-upload="beforeUpload"
          :file-list="fileList"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          list-type="picture-card"
        >
          <i class="el-icon-plus" />
        </el-upload>
        <el-dialog :visible.sync="imageVisible">
          <img width="100%" :src="imageUrl" alt="" />
        </el-dialog>
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
import ProjectApi from "../../request/project";
export default {
  props: ["title", "pid"],
  name: "projectDialog",
  data() {
    return {
      showTitle: "",
      imageUrl: "",
      imageVisible: false,
      dialogVisible: true,
      projectForm: {
        name: "",
        describe: "",
        image: "",
      },
      rules: {
        name: [{ required: true, message: "请输入项目名称", trigger: "blur" }],
      },
      fileList: [],
    };
  },
  mounted() {
    if (this.title === "create") {
      this.showTitle = "创建项目";
    } else if (this.title === "edit") {
      this.showTitle = "编辑项目";
      this.initProject();
    }
  },
  methods: {
    // 删除图片
    handleRemove(file) {
      console.log("删除", file);
    },
    // 预览图片
    handlePreview(file, fileList) {
      console.log(fileList);
      this.imageUrl = file.url;
      this.imageVisible = true;
    },
    closeDiglog() {
      this.$emit("cancel", {});
    },
    //获取项目详情
    async initProject() {
      const resp = await ProjectApi.getProject(this.pid);
      if (resp.success === true) {
        this.projectForm = resp.item;
        this.fileList.push({
          name: resp.item.image,
          url: "static/images/" + resp.item.image,
        });
        this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败");
      }
    },
    // 创建项目
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title === "create") {
            ProjectApi.createProject(this.projectForm).then((resp) => {
              if (resp.success === true) {
                this.closeDiglog();
                this.$message.success("创建成功！");
              } else {
                this.$message.error(resp.error.message);
              }
            });
          } else if (this.title === "edit") {
            ProjectApi.updateProject(this.pid, this.projectForm).then(
              (resp) => {
                if (resp.success === true) {
                  this.closeDiglog();
                  this.$message.success("编辑成功！");
                } else {
                  this.$message.error(resp.error.message);
                }
              }
            );
          }
        } else {
          return false;
        }
      });
    },
    beforeUpload(file) {
      console.log(file);
      let fd = new FormData();
      fd.append("file", file);

      ProjectApi.uploadImage(fd).then((resp) => {
        if (resp.data.success === true) {
          this.projectForm.image = resp.data.item.name;
          const imagePath = "/static/images/" + resp.data.item.name;
          console.log("imagePath", imagePath);
          this.fileList.push({
            name: file.name,
            url: imagePath,
          });
          this.$message.success("上传成功！");
        } else {
          console.log("上传失败", resp);
          this.$message.error(resp.error.message);
        }
      });
      return true;
    },
  },
};
</script>
