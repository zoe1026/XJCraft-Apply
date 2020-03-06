import Layout from '@/layout'

const playerRouter = {
  path: '/player',
  component: Layout,
  redirect: 'noRedirect',
  name: 'Player',
  meta: {
    title: '系统配置',
    roles: ['ADMIN']
  },
  children: [
    {
      path: 'demo',
      component: () => import('@/views/player/demo'),
      name: 'demo',
      meta: {
        title: 'demo'
      }
    }
  ]
}
export default playerRouter
