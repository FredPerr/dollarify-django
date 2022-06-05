const average_rate_card = document.getElementById('average_rate_card');
const ytd_revenu = document.getElementById('ytd-revenu');
const average_hours = document.getElementById('average-hours');
const total_revenu = document.getElementById('total-revenu');


average_rate_card.innerHTML = `${get_average_hourly_rate(paychecks)} $/H`;
ytd_revenu.innerHTML = `${get_ytd_revenu(paychecks)} $`;
average_hours.innerHTML = `${get_average_hours_per_week(paychecks)} H`;
total_revenu.innerHTML = `${get_total_amount(paychecks)} $`;