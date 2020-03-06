import Layout from '@/layout'

const playerRouter = {
  path: '/player',
  component: Layout,
  redirect: 'noRedirect',
  name: 'Player',
  meta: {
    title: '玩家申请',
    roles: ['OP']
  },
  children: [
    {
      path: 'req-list',
      component: () => import('@/views/player/req-list'),
      name: '玩家申请列表',
      meta: {
        title: '玩家申请列表'
      }
    }
  ]
}
export default playerRouter
