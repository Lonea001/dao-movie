import request from './request'

export const    getRankings     =   ()            =>  request.get('/rankings')
export const    getRanking      =   (id)          =>  request.get(`/rankings/${id}`)
export const    createRanking   =   (data)        =>  request.post('/rankings', data)
export const    updateRanking   =   (id, data)    =>  request.put(`/rankings/${id}`, data)
export const    deleteRanking   =   (id)          =>  request.delete(`/rankings/${id}`)