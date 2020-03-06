import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import qs from 'qs'
// import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 30000 // request timeout
})

let logoutLock = false

// request interceptor
service.interceptors.request.use(
  config => {
    config.paramsSerializer = (params) => {
      return qs.stringify(params, { arrayFormat: 'repeat' })
    }

    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data

    // if the custom code is not 20000, it is judged as an error.
    if (res.code < 0) {
      if (!logoutLock) {
        Message({
          message: res.message || 'Error',
          type: 'error',
          duration: 5 * 1000
        })
      }

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (res.code === -2) {
        // to re-login
        if (logoutLock) return
        logoutLock = true

        MessageBox.confirm('您的登陆已过期，您可以重新登陆，或取消继续留在此页面。', '重新登陆', {
          confirmButtonText: '重新登陆',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/resetToken').then(() => {
            location.reload()
          })
        })
      }
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res
    }
  },
  error => {
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
