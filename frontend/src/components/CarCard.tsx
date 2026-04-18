import { Car } from "../types";
import { Shield, Fuel, Gauge, Users, Star, Zap } from "lucide-react";

interface Props {
  car: Car;
}

function SafetyStars({ rating }: { rating: number }) {
  return (
    <div className="flex items-center gap-0.5">
      {Array.from({ length: 5 }).map((_, i) => (
        <Star
          key={i}
          size={12}
          className={i < rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"}
        />
      ))}
    </div>
  );
}

export default function CarCard({ car }: Props) {
  const isEV = car.fuel_type === "Electric";

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-gray-900">
            {car.make} {car.model}
          </h3>
          <p className="text-sm text-gray-500">{car.variant}</p>
        </div>
        <span className="text-lg font-bold text-blue-600">
          ₹{car.price_lakhs}L
        </span>
      </div>

      {/* Quick Specs */}
      <div className="grid grid-cols-2 gap-2 mb-3 text-sm">
        <div className="flex items-center gap-1.5 text-gray-600">
          <Fuel size={14} className="text-gray-400" />
          <span>{car.fuel_type} · {car.transmission}</span>
        </div>
        <div className="flex items-center gap-1.5 text-gray-600">
          <Gauge size={14} className="text-gray-400" />
          <span>{isEV ? `${car.mileage_kmpl}km range` : `${car.mileage_kmpl} kmpl`}</span>
        </div>
        <div className="flex items-center gap-1.5 text-gray-600">
          <Zap size={14} className="text-gray-400" />
          <span>{car.power_hp} hp</span>
        </div>
        <div className="flex items-center gap-1.5 text-gray-600">
          <Users size={14} className="text-gray-400" />
          <span>{car.seating_capacity} seats</span>
        </div>
      </div>

      {/* Safety */}
      <div className="flex items-center gap-2 mb-3">
        <Shield size={14} className="text-green-600" />
        <span className="text-xs text-gray-500">NCAP</span>
        <SafetyStars rating={car.safety_rating_ncap} />
        <span className="ml-auto flex items-center gap-1 text-xs text-gray-500">
          <Star size={12} className="fill-yellow-400 text-yellow-400" />
          {car.user_rating}
        </span>
      </div>

      {/* Key Features */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        {car.key_features.slice(0, 4).map((f) => (
          <span
            key={f}
            className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full"
          >
            {f}
          </span>
        ))}
        {car.key_features.length > 4 && (
          <span className="text-xs text-gray-400">
            +{car.key_features.length - 4} more
          </span>
        )}
      </div>

      {/* Pros/Cons */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div>
          {car.pros.slice(0, 2).map((p) => (
            <p key={p} className="text-green-700 mb-0.5">+ {p}</p>
          ))}
        </div>
        <div>
          {car.cons.slice(0, 2).map((c) => (
            <p key={c} className="text-red-600 mb-0.5">- {c}</p>
          ))}
        </div>
      </div>
    </div>
  );
}
