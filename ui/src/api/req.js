import request from '@/utils/request'

export function req(data) {
  return request({
    url: '/player/req',
    method: 'post',
    data
  })
}

export function fetchReqList(params) {
  return request({
    url: '/req/list',
    method: 'get',
    params
  })
}

export function apply(data) {
  return request({
    url: '/req/apply',
    method: 'post',
    data
  })
}
