import { CarComparison } from "../types";

interface Props {
  comparison: Record<string, CarComparison>;
}

const ROWS: { label: string; key: keyof CarComparison; format?: (v: unknown) => string }[] = [
  { label: "Price", key: "price_lakhs", format: (v) => `₹${v}L` },
  { label: "Body Type", key: "body_type" },
  { label: "Fuel", key: "fuel_type" },
  { label: "Transmission", key: "transmission" },
  { label: "Engine", key: "engine_cc", format: (v) => `${v}cc` },
  { label: "Power", key: "power_hp", format: (v) => `${v} hp` },
  { label: "Torque", key: "torque_nm", format: (v) => `${v} Nm` },
  { label: "Mileage", key: "mileage_kmpl", format: (v) => `${v} kmpl` },
  { label: "Safety (NCAP)", key: "safety_rating_ncap", format: (v) => `${v}★` },
  { label: "Seats", key: "seating_capacity" },
  { label: "User Rating", key: "user_rating", format: (v) => `${v}/5` },
];

export default function ComparisonTable({ comparison }: Props) {
  const carIds = Object.keys(comparison);

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-blue-50">
            <th className="text-left p-2 font-medium text-gray-500 border-b">Spec</th>
            {carIds.map((id) => (
              <th key={id} className="text-left p-2 font-semibold text-gray-900 border-b">
                {comparison[id].make} {comparison[id].model}
                <span className="block text-xs font-normal text-gray-500">
                  {comparison[id].variant}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {ROWS.map((row) => (
            <tr key={row.key} className="border-b border-gray-100 hover:bg-gray-50">
              <td className="p-2 text-gray-500 font-medium">{row.label}</td>
              {carIds.map((id) => {
                const val = comparison[id][row.key];
                return (
                  <td key={id} className="p-2 text-gray-900">
                    {row.format ? row.format(val) : String(val)}
                  </td>
                );
              })}
            </tr>
          ))}
          {/* Key Features Row */}
          <tr className="border-b border-gray-100">
            <td className="p-2 text-gray-500 font-medium align-top">Features</td>
            {carIds.map((id) => (
              <td key={id} className="p-2">
                <div className="flex flex-wrap gap-1">
                  {comparison[id].key_features?.slice(0, 5).map((f) => (
                    <span key={f} className="text-xs bg-gray-100 px-1.5 py-0.5 rounded">
                      {f}
                    </span>
                  ))}
                </div>
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}
