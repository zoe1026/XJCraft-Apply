<template lang="pug">
  .login-container
    .app-container
      .title-container
        h3.title 注册申请

      el-steps(style={ width: '520px', margin: '0 auto' }, :active="step", finish-status="success")
        el-step(title="阅读规则")
        el-step(title="小测验")
        el-step(title="提交申请")
        el-step(title="完成申请")

      div.paddintop(v-if="step === 0", align="center")
        div
          span 请下载并阅读规则哟(提取码 hvcn)
        div(style={ 'margin-top': '32px' })
          el-button(:disabled="step0.step >= 1 && step0.step < step0.waitTime", @click="clickStep0") {{ step0.btnName }}

      div.paddintop(v-else-if="step === 1", style={ width: '600px', margin: '0 auto', color: '#eee' })
        div(v-for="(qa, idx) in step1.qa", :key="idx", style={ 'margin-top': '8px' })
          p(v-if="qa.type !== 'input'")
           span {{ idx + 1 }}.&nbsp;
           span {{ qa.question }}
           span &nbsp;({{ qa.score }}分)
          p(v-else)
            span {{ idx + 1 }}.&nbsp;
            span.inputType(v-for="(q, idx2) in qa.question", :key="idx2")
              span(v-if="q") {{ q }}
              el-input(v-else, v-model="qa.player[(idx2 - 1) / 2]")
            span &nbsp;({{ qa.score }}分)
          div(style={ 'margin-left': '20px' })
            div(v-if="qa.type === 'radio'")
              el-radio-group(v-model="qa.player")
                div(v-for="(a, idx3) in qa.answer", :key="idx3")
                  el-radio(:label="idx3", style={ color: '#eee', 'margin-top': '8px' }) {{ a }}
            div(v-else-if="qa.type === 'checkbox'")
              el-checkbox-group(v-model="qa.player")
                div(v-for="(a, idx3) in qa.answer", :key="idx3")
                  el-checkbox(:label="idx3", style={ color: '#eee', 'margin-top': '8px' }) {{ a }}
            div(v-else-if="qa.type === 'switch'")
              el-radio-group(v-model="qa.player")
                el-radio(:label="false", style={ color: '#eee', 'margin-top': '8px' }) {{ (qa.answer && qa.answer[0]) || '错误' }}
                el-radio(:label="true", style={ color: '#eee', 'margin-top': '8px' }) {{ (qa.answer && qa.answer[1]) || '正确' }}

        div(style={ 'margin-top': '50px' }, align="center")
          el-button(:disabled="step1.wait >= 1", @click="clickStep1") {{ step1.btnName }}

      div.paddintop(v-else-if="step === 2")
        el-form.login-form(ref="reqForm", :model="reqForm", :rules="reqRules", autocomplete="off", label-position="left")
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

          el-button(:loading="loading", type="primary", style="width: 100%; margin-bottom: 30px;", @click.native.prevent="handleReq") 提交申请

      div.paddintop(v-else-if="step === 3", align="center")
        div 申请成功，请耐心等待 OP 处理
        div(style={ 'margin-top': '32px' })
          el-button(@click="clickStep3") 查询处理进度
</template>

<script>
import { validUsername } from '@/utils/validate'
import { req } from '@/api/req'
import { notifySuccess, notifyWarn } from '../../utils/notify'

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
      step: this.$route.query.skip === 'xj' ? Number(this.$route.query.step) : 0,
      step0: {
        btnName: '点击下载规则',
        step: 0,
        waitTime: 301 // 设置为等待的秒数 + 1
      },
      step1: {
        // 题目
        qa: [
          { // 单选题
            type: 'radio',
            question: '单选题 - 合成一个工作台需要几个木板？',
            answer: [
              '1',
              '2',
              '3',
              '4'
            ],
            score: 5,
            correct: 3,
            player: -1
          },
          { // 多选题
            type: 'checkbox',
            question: '多选题 - 哪些是合成信标需要的材料？',
            answer: [
              '沙子',
              '黑曜石',
              '水桶',
              '玻璃'
            ],
            score: 5,
            correct: [1, 3],
            player: []
          },
          { // 判断题
            type: 'switch',
            question: '判断题 - 在服务器里可以随便熊',
            score: 5,
            correct: false,
            player: void 0
          },
          { // 判断题，自定义错误和正确的内容，第一个对应 false，第二个对应 true
            type: 'switch',
            question: '判断题 - 服务器里可以熊么？',
            answer: ['不可以', '可以'],
            score: 5,
            correct: false,
            player: void 0
          },
          { // 填空题
            type: 'input',
            // 注意，最后一个空就在结尾时，即使后面什么都没有，也要写点什么，比如句号，甚至一个空字符串: ''
            // 同理，第一个空在开头时，前面也要写点什么，哪怕是个空字符串
            question: ['填空题 - 合成一个信标需要', '个黑曜石、', '个玻璃、以及一个', '。'],
            score: 5,
            correct: [
              // 每个数组是一个空的答案，填里面任意一个都算对，判题的时候会自动去掉两变的空格，因此答案里也不要带两边空格
              // 对于字母，会忽略大小写
              ['3', '三'],
              ['5', '五'],
              ['下界之星', '星星', 'Nether Star', 'NetherStar', 'Star']
            ],
            player: []
          }

          // 以上为示例，问题请参照上面的往后加

        ],
        // 所有题目总分数(自动计算)
        totalScore: -1,
        // 最低多少分可以过
        minScore: 20,
        btnName: '答题完毕，下一步',
        wait: 0
      },
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
      loading: false
    }
  },
  mounted() {
    let totalScore = 0
    for (let i = this.step1.qa.length - 1; i >= 0; i--) {
      const qa = this.step1.qa[i]
      totalScore += qa.score
      if (qa.type === 'input') {
        for (let j = qa.question.length - 1; j >= 1; j--) {
          qa.question.splice(j, 0, void 0)
        }
      }
    }
    this.totalScore = totalScore

    console.log('总分: ' + totalScore)
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
            notifySuccess('申请成功')
            this.loading = false
            this.step += 1
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    clickStep0() {
      if (this.step0.step === 0) {
        window.open('https://pan.baidu.com/s/1xS2xf6SsiOrK-ctMrQVHOA')

        let h = -1
        const code = () => {
          this.step0.step += 1
          if (this.step0.step === this.step0.waitTime) {
            this.step0.btnName = '已阅读，下一步'
            clearInterval(h)
          } else {
            this.step0.btnName = '已阅读，下一步(' + (this.step0.waitTime - this.step0.step) + ')'
          }
        }
        h = setInterval(code, 1000)
        code()
      } else if (this.step0.step === this.step0.waitTime) {
        this.step += 1
      }
    },
    clickStep1() {
      let score = 0
      this.step1.qa.forEach(e => {
        switch (e.type) {
          case 'radio':
            if (e.correct === e.player) score += e.score
            break
          case 'checkbox':
            if (e.correct.length === e.player.length) {
              if (!e.correct.find(a => e.player.indexOf(a) < 0)) {
                score += e.score
              }
            }

            score += e.score
            break
          case 'switch':
            if (e.correct === e.player) score += e.score
            break
          case 'input':
            let err = false
            for (let i = e.correct.length - 1; i >= 0; i--) {
              if (e.correct[i].indexOf(e.player[i]) < 0) {
                err = true
                break
              }
            }
            if (!err) score += e.score

            break
        }
      })

      if (score > this.step1.minScore) {
        this.step += 1
      } else {
        notifyWarn('您答错的有点多呢，再努力下试试吧~')
        let h = -1
        this.step1.wait = 120
        const code = () => {
          this.step1.wait -= 1
          if (this.step1.wait === 0) {
            this.step1.btnName = '答题完毕，下一步'
            clearInterval(h)
          } else {
            this.step1.btnName = '答题完毕，下一步(' + (this.step1.wait) + ')'
          }
        }
        h = setInterval(code, 1000)
        code()
      }
    },
    clickStep3() {
      this.$router.push({ name: '查询申请进度', params: { playerName: this.reqForm.playerName, qq: this.reqForm.qq }})
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

.inputType {
  .el-input {
    width: 100px;

    input {
      background-color: #47586e;
      border-top-width: 0px;
      border-left-width: 0px;
      border-right-width: 0px;
      border-bottom-width: 1px;
      border-radius: 0px;
    }
  }
}

/* reset element-ui css */
.login-container {
  .login-form {
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
}
</style>

<style lang="scss" scoped>
$bg:#47586e;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .paddintop {
    padding: 100px 35px 0;
  }

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
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
}
</style>
