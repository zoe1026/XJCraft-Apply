<template lang="pug">
  .login-container
    el-form(ref="reqForm", :model="reqForm", :rules="reqRules", class="login-form", autocomplete="off", label-position="left")
      .title-container
        h3.title 注册申请

      el-form-item(prop="playerName")
        el-input(
          ref="playerName",
          v-model="reqForm.playerName",
          placeholder="玩家名",
          name="playerName",
          type="text",
          tabindex="1"
        )

      el-tooltip(v-model="capsTooltip", content="大写锁定已开启", placement="right", manual)
        el-form-item(prop="password")
          el-input(
            :key="passwordType",
            ref="password",
            v-model="reqForm.password",
            :type="passwordType",
            placeholder="密码",
            name="password",
            tabindex="2",
            autocomplete="on",
            @keyup.native="checkCapslock",
            @blur="capsTooltip = false",
            @keyup.enter.native="handleLogin"
          )
          span.show-pwd(@click="showPwd")
            svg-icon(:icon-class="passwordType === 'password' ? 'eye' : 'eye-open'")

      el-form-item(prop="qq")
        el-input(
          ref="qq",
          v-model="reqForm.qq",
          placeholder="QQ 号",
          name="qq",
          type="text",
          tabindex="3"
        )

      el-form-item(prop="type")
        el-select(
          ref="type",
          v-model="reqForm.type",
          placeholder="申请类型",
          name="type",
          tabindex="4",
          style="width: 100%"
        )
          el-option(key="", label="请选择申请类型", value="")
          el-option(key="QQLevel", label="QQ 等级已达到太阳", value="QQLevel")
          el-option(key="Invite", label="老玩家邀请", value="Invite")
          el-option(key="PYJY", label="与 OP 协商", value="PYJY")

      el-form-item(v-if="reqForm.type === 'Invite'", prop="oldPlayerName")
        el-input(
          ref="oldPlayerName",
          v-model="reqForm.oldPlayerName",
          placeholder="邀请人(玩家名)",
          name="oldPlayerName",
          type="text",
          tabindex="3"
        )

      el-form-item(v-if="reqForm.type === 'PYJY'", prop="opName")
        el-input(
          ref="opName",
          v-model="reqForm.opName",
          placeholder="OP(玩家名)",
          name="opName",
          type="text",
          tabindex="3"
        )

      el-button(:loading="loading", type="primary", style="width:100%;margin-bottom:30px;", @click.native.prevent="handleReq") 提交申请
</template>

<script>
import { validUsername } from '@/utils/validate'
import { req } from '@/api/req'
import { notifySuccess } from '../../utils/notify'

export default {
  name: 'Req',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('请输入有效的玩家名(大小写字母、数字和下划线，3 ~ 16 位)'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于 6 位'))
      } else if (value.length > 50) {
        callback(new Error('密码不能多于 50 位'))
      } else {
        callback()
      }
    }
    const validateQQ = (rule, value, callback) => {
      if (/^\d{5,11}$/.test(value)) {
        callback()
      } else {
        callback(new Error('请输入有效的 QQ 号'))
      }
    }
    const validateType = (rule, value, callback) => {
      if (value !== '') {
        callback()
      } else {
        callback(new Error('请选择申请类型'))
      }
    }
    return {
      reqForm: {
        playerName: '',
        password: '',
        qq: '',
        type: '',
        oldPlayerName: '',
        opName: ''
      },
      reqRules: {
        playerName: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        qq: [{ required: true, trigger: 'blur', validator: validateQQ }],
        type: [{ required: true, trigger: 'blur', validator: validateType }],
        oldPlayerName: [{ required: () => this.type === 'Invite', trigger: 'blur', validator: validateUsername }],
        opName: [{ required: () => this.type === 'PYJY', trigger: 'blur', validator: validateUsername }]
      },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      showDialog: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  methods: {
    checkCapslock(e) {
      const { key } = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleReq() {
      this.$refs.reqForm.validate(valid => {
        if (valid) {
          this.loading = true
          req(this.reqForm).then(response => {
            notifySuccess(response.data || '申请成功，请耐心等待处理，处理结果将在群内通过 QQ 通知，重新输入同样的信息可查询处理进度', { timeout: 15000 })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
