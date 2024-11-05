import { useContext } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import { RealtimeDataContext } from "../realtime/realtime_data_context";

export function MemoryInfoView() {
  const data = useContext(RealtimeDataContext);

  function getMemoryObj() {
    var obj: any = data[data.length - 1];
    if (obj === undefined) return {};
    return obj
  }

  return (
    <div className="flex flex-row h-full gap-6">
      <div className="flex flex-col h-[90%] flex-1">
        <ResponsiveContainer className="flex-1" width="100%">
          <AreaChart data={data} className="bg-popover rounded-lg">
            <defs>
              <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.8} />
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis hide />
            <YAxis domain={[0, 100]} hide />
            <CartesianGrid strokeDasharray="9 9" opacity={0.25} />
            <Area
              type="monotone"
              dataKey="memory_percent"
              stroke="hsl(var(--primary))"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
          </AreaChart>
        </ResponsiveContainer>

        <div className="pt-4 text-5xl font-bold">Memory Graph</div>
      </div>

      <div className="flex flex-col gap-8 pr-56">
        <div>
            <div className="text-4xl font-semibold pb-2">Utilization</div>
            <div>{getMemoryObj().memory_percent || "Unknown"}%</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Virtual Memory</div>
            <div>{(getMemoryObj().virtual_memory / 1024 / 1024 / 1024).toFixed(2) || "Unknown"} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Swap Memory</div>
            <div>{(getMemoryObj().swap_memory / 1024 / 1024 / 1024).toFixed(2) || "Unknown"} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Used</div>
            <div>{(getMemoryObj().memory_usage / 1024 / 1024 / 1024).toFixed(2) || "Unknown"} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Available</div>
            <div>{(getMemoryObj().memory_available / 1024 / 1024 / 1024).toFixed(2) || "Unknown"} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Total</div>
            <div>{(getMemoryObj().memory_total / 1024 / 1024 / 1024).toFixed(2) || "Unknown"} GB</div>
        </div>

      </div>
    </div>
  );
}
