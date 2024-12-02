// app/page.tsx
import React from 'react'

type Event = {
  type: string
  player: string
  minute: number
}

type MatchData = {
  matchId: number
  homeTeam: string
  awayTeam: string
  events: Event[]
}

async function getMatchData(): Promise<MatchData> {
  const res = await fetch('https://api.statsbomb.com/matches/12345/events', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY'  // Reemplaza con tu clave de API de StatsBomb
    }
  })

  if (!res.ok) {
    throw new Error('Failed to fetch match data')
  }

  const data = await res.json()

  // Aquí puedes personalizar según la respuesta de la API
  return {
    matchId: 12345,
    homeTeam: 'Team A',
    awayTeam: 'Team B',
    events: data.map((event: any) => ({
      type: event.type,
      player: event.player_name,
      minute: event.minute
    }))
  }
}

const Dashboard = async () => {
  let matchData: MatchData | null = null

  try {
    matchData = await getMatchData()
  } catch (error) {
    console.error('Error fetching match data:', error)
  }

  if (!matchData) {
    return <div>Error loading match data</div>
  }

  return (
    <div>
      <h1>Dashboard del Partido</h1>
      <h2>{matchData.homeTeam} vs {matchData.awayTeam}</h2>
      
      <h3>Eventos del Partido</h3>
      <ul>
        {matchData.events.map((event, index) => (
          <li key={index}>
            <strong>{event.type}</strong> - {event.player} en el minuto {event.minute}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Dashboard
