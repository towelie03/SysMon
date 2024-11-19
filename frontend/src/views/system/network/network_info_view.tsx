import { useContext, useEffect, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import { RealtimeDataContext } from "../realtime/realtime_data_context";

export function NetworkInfoView() {
  const realtimeData = useContext(RealtimeDataContext);
  const [network_data, setNetworkData] = useState<any>({});

  function getUptime() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.uptime.toFixed(0);
  }

  function getSent() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.throughput.sent.toFixed(0);
  }

  function getRecieved() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.throughput.recv.toFixed(0);
  }

  useEffect(() => {
    async function asyncBridge() {
        const respone = await fetch("http://127.0.0.1:8000/network/all")
        const result = await respone.json()

        setNetworkData(result)
    }

    asyncBridge()
  }, []);

  return (
    <div className="flex flex-row h-full gap-6">
      <div className="flex flex-col h-[90%] flex-1">
        <ResponsiveContainer className="flex-1" width="100%">
          <AreaChart data={realtimeData} className="bg-popover rounded-lg">
            <defs>
              <linearGradient id="colorSent" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.8} />
                <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorRecv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--chart-2))" stopOpacity={0.8} />
                <stop offset="95%" stopColor="hsl(var(--chart-2))" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis hide />
            <YAxis domain={[0, 100_000]} hide />
            <Legend className="pt-4"/>
            <CartesianGrid strokeDasharray="9 9" opacity={0.25} />
            <Area
              type="monotone"
              dataKey="throughput.sent"
              stroke="hsl(var(--chart-1))"
              fillOpacity={1}
              fill="url(#colorSent)"
              min={0}
              max={100_000}
            />
            <Area
              type="monotone"
              dataKey="throughput.recv"
              stroke="hsl(var(--chart-2))"
              fillOpacity={1}
              fill="url(#colorRecv)"
              min={0}
              max={100_000}
            />
          </AreaChart>
        </ResponsiveContainer>

        <div className="pt-4 text-5xl font-bold">Network Graph</div>
      </div>

      <div className="flex flex-col gap-8 pr-56">
        <div>
            <div className="text-4xl font-semibold pb-2">Sent</div>
            <div>{getSent()} Kbps</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Recieved</div>
            <div>{getRecieved()} Kbps</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Connection Type</div>
            <div>{network_data.type}</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">IPV4 Address</div>
            <div>{network_data.ipv4}</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">IPV6 Address</div>
            <div>{network_data.ipv6}</div>
        </div>
      </div>
    </div>
  );
}
