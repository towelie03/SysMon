import { useContext, useEffect, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import { RealtimeDataContext } from "../realtime/realtime_data_context";

export function CpuInfoView() {
  const realtimeData = useContext(RealtimeDataContext);
  const [cpu_data, setCpuData] = useState<any>({});

  function getCpuUsage() {
    if (realtimeData[realtimeData.length - 1] == undefined) {
      return "Unkown";
    }

    return realtimeData[realtimeData.length - 1].cpu_usage;
  }

  function getCpuFrequency() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.cpu_frequency.current.toFixed(0);
  }

  function getUptime() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.uptime.toFixed(0);
  }

  useEffect(() => {
    async function asyncBridge() {
        const respone = await fetch("http://127.0.0.1:8000/cpu/all")
        const result = await respone.json()

        setCpuData(result)
    }

    asyncBridge()
  }, []);

  return (
    <div className="flex flex-row h-full gap-6">
      <div className="flex flex-col h-[90%] flex-1">
        <ResponsiveContainer className="flex-1" width="100%">
          <AreaChart data={realtimeData} className="bg-popover rounded-lg">
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
              dataKey="cpu_usage"
              stroke="hsl(var(--primary))"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
          </AreaChart>
        </ResponsiveContainer>

        <div className="pt-4 text-5xl font-bold">CPU Graph</div>
      </div>

      <div className="flex flex-col gap-8 pr-56">
        <div>
            <div className="text-4xl font-semibold pb-2">Name</div>
            <div>{cpu_data.cpu_name || "Unknown"}</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Utilization</div>
            <div>{getCpuUsage()}%</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Speed</div>
            <div>{getCpuFrequency()} Mhz</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Count</div>
            <div>{cpu_data.cpu_count ?? 0}</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Temperature</div>
            <div>{cpu_data.cpu_temperature ?? 0} °C</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Uptime</div>
            <div>{getUptime()} s</div>
        </div>

      </div>
    </div>
  );
}
