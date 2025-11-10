# রিলেটেড পোস্ট ইনসার্ট ফিচার

## কিভাবে ব্যবহার করবেন:

### ১. এডমিন প্যানেলে যান
- Post বা Portfolio add/edit page এ যান
- Content বা Description editor দেখবেন

### ২. রিলেটেড পোস্ট বাটন
- Editor এর toolbar এ **"রিলেটেড পোস্ট"** বাটন দেখবেন (🔗 icon সহ)
- এই বাটনে ক্লিক করুন

### ৩. পোস্ট সার্চ করুন
- একটি মোডাল/popup খুলবে
- Search box এ পোস্ট এর নাম টাইপ করুন (কমপক্ষে ২ অক্ষর)
- Real-time search results দেখবেন

### ৪. পোস্ট সিলেক্ট করুন
- Search results এ যে পোস্ট দেখাবে, তাতে ক্লিক করুন
- Automatically সেই পোস্টের লিঙ্ক content এ insert হবে

### ৫. সেভ করুন
- Post/Portfolio save করুন
- Frontend এ লিঙ্কটি card style এ দেখাবে

## Features:
✅ Real-time search (300ms debounce)
✅ পোস্ট টাইটেল এবং content এ search করে
✅ সর্বোচ্চ 10টি result দেখায়
✅ Beautiful modal UI with hover effects
✅ Bangla interface
✅ Auto-insert link with post title
✅ Frontend এ card style display

## Technical Details:

### Backend:
- **Endpoint**: `/search-posts/`
- **Method**: GET
- **Parameter**: `q` (query string)
- **Response**: JSON with posts array

### Frontend:
- **Custom Summernote Button**: "রিলেটেড পোস্ট"
- **Search Modal**: Real-time search with AJAX
- **Link Insertion**: Uses Summernote's `createLink` API

### Files Modified:
1. `mini/views.py` - Added `search_posts` view
2. `mini/urls.py` - Added `/search-posts/` URL
3. `templates/admin/mini/post/change_form.html` - Custom button & modal
4. `templates/admin/mini/portfolio/change_form.html` - Same features

## Example Usage:
1. লিখছেন: "এই বিষয়ে আরও জানতে..."
2. "রিলেটেড পোস্ট" button ক্লিক করুন
3. Search করুন: "Python Tutorial"
4. Result এ "Python Basics" ক্লিক করুন
5. Link insert হবে: "Python Basics" (clickable)
6. Frontend এ card হিসেবে দেখাবে সুন্দর style এ
