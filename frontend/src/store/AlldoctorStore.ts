// @/lib/doctor-store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface Doctor {
  id: number
  name: string
  specialization: string 
}

interface DoctorState {
  doctors: Doctor[]
  setDoctors: (data: Doctor[]) => void
}

export const useAllDoctorStore = create<DoctorState>()(
  persist(
    (set) => ({
      doctors: [],
      setDoctors: (data) => set({ doctors: data }),
    }),
    {
      name: 'all-doctor-storage',
    }
  )
)
