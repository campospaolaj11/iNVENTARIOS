interface StatsCardProps {
  title: string
  value: string | number
  icon: string
  color: 'blue' | 'red' | 'green' | 'orange'
}

const colorClasses = {
  blue: 'from-blue-500 to-blue-700',
  red: 'from-red-500 to-red-700',
  green: 'from-green-500 to-green-700',
  orange: 'from-orange-500 to-orange-700'
}

function StatsCard({ title, value, icon, color }: StatsCardProps) {
  return (
    <div className={`stat-card bg-gradient-to-br ${colorClasses[color]} animate-slide-up`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-white/80 text-sm font-medium uppercase tracking-wide">{title}</p>
          <p className="text-4xl font-bold mt-3 mb-1">{value}</p>
          <div className="h-1 w-16 bg-white/30 rounded-full mt-2"></div>
        </div>
        <div className="text-5xl opacity-80 transform transition-transform duration-300 hover:scale-110">
          {icon}
        </div>
      </div>
    </div>
  )
}

export default StatsCard
