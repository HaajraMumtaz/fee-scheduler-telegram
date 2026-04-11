import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    const { callback_query } = await req.json()
    
    if (callback_query) {
      const supabase = createClient(
        Deno.env.get('SUPABASE_URL')!,
        Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
      )

      // Data format from button: "pay:fee_id"
      const [action, feeId] = callback_query.data.split(':')

      if (action === 'pay') {
        await supabase
          .from('monthly_fees')
          .update({ status: 'paid', paid_on: new Date().toISOString() })
          .eq('id', feeId)
      }
    }

    return new Response(JSON.stringify({ ok: true }), { 
      headers: { "Content-Type": "application/json" } 
    })
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 })
  }
})