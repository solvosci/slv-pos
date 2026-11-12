import { PosPreset } from "@point_of_sale/app/models/pos_preset";
import { patch } from "@web/core/utils/patch";

const { DateTime } = luxon;

patch(PosPreset.prototype, {
    // Copy of the core method: the only change is the number of days,
    // read from the preset instead of the hardcoded 7.
    generateSlots() {
        const now = DateTime.now();
        const usage = this.slotsUsage;
        const interval = this.interval_time;
        const slots = {};
        const days = this.slot_days || 7;

        for (const i of [...Array(days).keys()]) {
            const dateNow = now.plus({ days: i });
            const getDateTime = (hour) =>
                DateTime.fromObject({
                    year: dateNow.year,
                    month: dateNow.month,
                    day: dateNow.day,
                    hour: Math.floor(hour),
                    minute: Math.round((hour % 1) * 60),
                });
            const dayOfWeek = (dateNow.weekday - 1).toString();
            const date = dateNow.toFormat("yyyy-MM-dd");
            const attToday = this.attendance_ids.filter((a) => a.dayofweek === dayOfWeek);
            slots[date] = [];

            for (const attendance of attToday) {
                const dateOpening = getDateTime(attendance.hour_from);
                const dateClosing = getDateTime(attendance.hour_to);

                let start = dateOpening;
                while (start >= dateOpening && start <= dateClosing && interval > 0) {
                    if (start >= now) {
                        const sqlDatetime = start.toFormat("yyyy-MM-dd HH:mm:ss");

                        if (slots[date][sqlDatetime]) {
                            slots[date][sqlDatetime].order_ids.add(...(usage[sqlDatetime] || []));
                        } else {
                            slots[date][sqlDatetime] = {
                                periode: attendance.day_period,
                                datetime: start,
                                order_ids: new Set(usage[sqlDatetime] || []),
                            };
                        }
                    }
                    start = start.plus({ minutes: interval });
                }
            }
        }

        this.uiState.availabilities = slots;
    },
});
