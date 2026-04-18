export interface Message {
  role: "user" | "assistant";
  content: string;
  cars?: Car[] | null;
  comparison?: Record<string, CarComparison> | null;
}

export interface Car {
  id: string;
  make: string;
  model: string;
  variant: string;
  price_lakhs: number;
  body_type: string;
  fuel_type: string;
  engine_cc: number;
  power_hp: number;
  torque_nm: number;
  transmission: string;
  mileage_kmpl: number;
  safety_rating_ncap: number;
  seating_capacity: number;
  key_features: string[];
  pros: string[];
  cons: string[];
  user_rating: number;
  review_summary: string;
  best_for: string[];
}

export interface CarComparison {
  make: string;
  model: string;
  variant: string;
  price_lakhs: number;
  body_type: string;
  fuel_type: string;
  engine_cc: number;
  power_hp: number;
  torque_nm: number;
  transmission: string;
  mileage_kmpl: number;
  safety_rating_ncap: number;
  seating_capacity: number;
  key_features: string[];
  pros: string[];
  cons: string[];
  user_rating: number;
  review_summary: string;
}

export interface ChatResponse {
  reply: string;
  cars?: Car[] | null;
  comparison?: Record<string, CarComparison> | null;
}
