interface StatsCardProps {
  title: string
  value: string | number
  icon: string
  color: 'blue' | 'red' | 'green' | 'orange'
}

const colorClasses = {
  blue: 'from-blue-500 via-blue-600 to-blue-700',
  red: 'from-red-500 via-red-600 to-red-700',
  green: 'from-emerald-500 via-green-600 to-green-700',
  orange: 'from-orange-500 via-orange-600 to-orange-700'
}

const shadowClasses = {
  blue: 'shadow-blue-500/50',
  red: 'shadow-red-500/50',
  green: 'shadow-emerald-500/50',
  orange: 'shadow-orange-500/50'
}

function StatsCard({ title, value, icon, color }: StatsCardProps) {
  return (
    <div className={`group relative stat-card bg-gradient-to-br ${colorClasses[color]} ${shadowClasses[color]} animate-slide-up overflow-hidden`}>
      {/* Efecto de brillo animado */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 animate-shimmer"></div>
      </div>
      
      {/* Patrón de fondo */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
          backgroundSize: '24px 24px'
        }}></div>
      </div>
      
      <div className="relative flex items-start justify-between">
        <div className="flex-1">
          <p className="text-white/90 text-xs font-bold uppercase tracking-wider mb-2">{title}</p>
          <p className="text-5xl font-black mt-2 mb-3 text-white drop-shadow-lg">{value}</p>
          <div className="flex items-center gap-2">
            <div className="h-1.5 w-20 bg-white/40 rounded-full overflow-hidden">
              <div className="h-full bg-white rounded-full animate-pulse" style={{width: '70%'}}></div>
            </div>
            <span className="text-white/60 text-xs font-medium">En tiempo real</span>
          </div>
        </div>
        <div className="relative">
          <div className="absolute inset-0 bg-white/20 blur-xl rounded-full"></div>
          <div className="relative text-6xl filter drop-shadow-2xl transform transition-all duration-300 group-hover:scale-125 group-hover:rotate-12">
            {icon}
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatsCard
