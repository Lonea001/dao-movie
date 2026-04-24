
export const posterUrl = (movieId) => `/api/posters/${movieId}`

export const fallbackPoster = 'https://via.placeholder.com/240x340?text=暂无海报'

export const handlePosterError = (e) => {
    e.target.src = fallbackPoster
}