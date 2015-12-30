import (
	"net/url"
	"encoding/json"
	"log"
)

func fetch(q *Query) bool {
	ok, res := utils.HttpGet(API + url.QueryEscape(q.query))
	if !ok {
		return false
	}
	var f map[string]interface{}
	if err := json.Unmarshal([]byte(res), &f); err != nil {
		return false
	}
	m := f["output"].(map[string]interface{})
	if val := m["val"]; val != "" {
		q.result = val.(string)
		log.Printf("[FETCH] %s", q.result)
		return true
	}
	return false
}
