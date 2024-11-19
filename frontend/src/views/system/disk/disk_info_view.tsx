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

export function DiskInfoView() {
  const realtimeData = useContext(RealtimeDataContext);
  const [disk_data, setdiskData] = useState<any>({});

  function getDiskUsage() {
    if (realtimeData[realtimeData.length - 1] == undefined) {
      return "Unknown";
    }

    return realtimeData[realtimeData.length - 1].disk_active_time;
  }

  function BtoGB(input: number) {
    return (input / 1024 / 1024 / 1024).toFixed(2)
  }

  useEffect(() => {
    async function asyncBridge() {
        const respone = await fetch("http://127.0.0.1:8000/disk/all")
        const result = await respone.json()

        setdiskData(result)
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
              dataKey="disk_active_time"
              stroke="hsl(var(--primary))"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
          </AreaChart>
        </ResponsiveContainer>

        <div className="pt-4 text-5xl font-bold">Disk Active Time</div>
      </div>

      <div className="flex flex-col gap-8 pr-56">
        <div>
            <div className="text-4xl font-semibold pb-2">Name</div>
            <div>WD_BLACK SN750 SE 1TB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Active Time</div>
            <div>{getDiskUsage()}%</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Total</div>
            <div>{BtoGB(disk_data.usage?.total || 0)} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Used</div>
            <div>{BtoGB(disk_data.usage?.used || 0)} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Free</div>
            <div>{BtoGB(disk_data.usage?.free || 0)} GB</div>
        </div>

        <div>
            <div className="text-4xl font-semibold pb-2">Read Count</div>
            <div>{disk_data.io_counters?.read_count || 0}</div>
        </div>

      </div>
    </div>
  );
}
