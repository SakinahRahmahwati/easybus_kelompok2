import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://kzudqffpgsrvcvvgnkhv.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6dWRxZmZwZ3NydmN2dmdua2h2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIyMDk2MjQsImV4cCI6MjA2Nzc4NTYyNH0.3-dg2YslgPXbhOod4vLpsMy4FVqYEHkG-ItSQrGOANA'
export const supabase = createClient(supabaseUrl, supabaseKey)
