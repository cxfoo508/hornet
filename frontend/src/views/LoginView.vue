<template>
  <div class="home">
    <div style="text-align: -webkit-center; margin-top: 350px">
      <el-card class="box-card">
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
          <el-tab-pane label="登录" name="first">
            <el-form
              ref="form"
              :model="form"
              label-width="80px"
              label-position="left"
              :rules="rules"
            >
              <el-form-item label="用户名:" prop="username">
                <el-input v-model="form.username" />
              </el-form-item>
              <el-form-item label="密码:" prop="password">
                <el-input v-model="form.password" type="password" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit" style="width: 360px"
                  >登录</el-button
                >
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="注册" name="second"> 注册 </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
// import UserApi from "../request/user"
export default {
  data() {
    return {
      activeName: "first",
      form: {
        username: "",
        password: "",
      } /* eslint-disable */,
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { min: 5, max: 10, message: "长度在 5 到10 个字符", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入活动名称", trigger: "blur" },
          { min: 6, max: 15, message: "长度在 6 到15 个字符", trigger: "blur" },
        ],
      },
    };
  },

  methods: {
    onSubmit() {
      console.log("submit!");
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
  name: "HomeView",
  components: {
    // HelloWorld,
  },
};
</script>
<style>
.box-card {
  width: 480px;
}
.Absolute-Center {
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}
</style>
