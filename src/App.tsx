import './App.css'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { Separator } from './components/ui/separator'
import { Line, LineChart, ResponsiveContainer } from 'recharts'

const data = [
  {
    name: 'Page A',
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: 'Page B',
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: 'Page C',
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: 'Page D',
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: 'Page E',
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: 'Page F',
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: 'Page G',
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

function App() {
  return <div className='dark bg-background w-screen h-screen p-4'>
    <Tabs defaultValue="system" className='flex flex-col items-center w-full h-full'>
      <TabsList className='flex justify-center items-center w-fit'>
        <TabsTrigger value="processes">Processes</TabsTrigger>
        <TabsTrigger value="system">System</TabsTrigger>
      </TabsList>
      <TabsContent value="processes" className='text-white'>Change your password here.</TabsContent>
      <TabsContent value="system" className='text-white w-full h-full p-4 rounded-md bg-card ring-2 ring-accent mt-4'>
        <div className='flex flex-row w-full h-full'>
          <div className='bg-popover flex flex-col w-[30%] h-full gap-4 pr-4'>

            <div className='flex flex-row h-full w-full accent-chart-1'>
              <ResponsiveContainer height="100%" width="50%">
                <LineChart width={200} height={100} data={data} className='bg-muted h-full rounded-lg'>
                  <Line type="monotone" dataKey="pv" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
              <div className='w-[50%] pl-4 '>
                <div className='font-semibold text-3xl'>
                  CPU
                </div>
                <div className='mt-0 text-lg text-muted-foreground'>
                  39% 3.82Ghz
                </div>
              </div>
            </div>
            <Separator></Separator>

            <div className='flex flex-row h-full w-full'>
              <ResponsiveContainer height="100%" width="50%">
                <LineChart width={200} height={100} data={data} className='bg-muted h-full rounded-lg'>
                  <Line type="monotone" dataKey="pv" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
              <div className='w-[50%] pl-4 '>
                <div className='font-semibold text-3xl'>
                  Memory
                </div>
                <div className='mt-0 text-lg text-muted-foreground'>
                  9.81 / 31.8 GB (31%)
                </div>
              </div>
            </div>
            <Separator></Separator>

            <div className='flex flex-row h-full w-full'>
              <ResponsiveContainer height="100%" width="50%">
                <LineChart width={200} height={100} data={data} className='bg-muted h-full rounded-lg'>
                  <Line type="monotone" dataKey="pv" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
              <div className='w-[50%] pl-4 '>
                <div className='font-semibold text-3xl'>
                  Disk 0
                </div>
                <div className='mt-0 text-lg text-muted-foreground'>
                  SSD (5%)
                </div>
              </div>
            </div>
            <Separator></Separator>

            <div className='flex flex-row h-full w-full'>
              <ResponsiveContainer height="100%" width="50%">
                <LineChart width={200} data={data} className='bg-muted h-full rounded-lg'>
                  <Line type="monotone" dataKey="pv" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
              <div className='w-[50%] pl-4 '>
                <div className='font-semibold text-3xl'>
                  Network
                </div>
                <div className='mt-0 text-lg text-muted-foreground'>
                  20 Kbps
                </div>
              </div>
            </div>
            <Separator></Separator>
          </div>
          <div className='w-full bg-muted rounded-md p-4'>abcd</div>
        </div>
      </TabsContent>
    </Tabs>
  </div >
}

export default App
