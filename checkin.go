package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

var (
	baseUrl = "https://example.com"
	email   = "example@example.com"
	passwd  = "password"
)

type Response struct {
	Headers    http.Header
	StatusCode int
	Content    []byte
}

type RequestOptions struct {
	Headers map[string]string
	Data    []byte
}

func Get(url string, opt *RequestOptions) (*Response, error) {
	return Request("GET", url, opt)
}

func Post(url string, opt *RequestOptions) (*Response, error) {
	return Request("POST", url, opt)
}

func Request(method string, url string, opt *RequestOptions) (*Response, error) {
	var data []byte
	if opt != nil {
		data = opt.Data
	}
	client := &http.Client{}

	req, err := http.NewRequest(method, url, bytes.NewBuffer(data))
	if err != nil {
		return nil, err
	}

	if opt != nil {
		for k, v := range opt.Headers {
			req.Header.Set(k, v)
		}
	}

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	buf, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	return &Response{
		resp.Header,
		resp.StatusCode,
		buf,
	}, nil
}

func main() {
	resp, err := Post(
		baseUrl+"/api/token",
		&RequestOptions{
			Headers: map[string]string{
				"Content-Type": "application/json",
			},
			Data: []byte(`{"email":"` + email + `","passwd":"` + passwd + `"}`),
		},
	)
	if err != nil {
		fmt.Println(err)
		return
	}

	var data map[string]interface{}
	err = json.Unmarshal(resp.Content, &data)
	if err != nil {
		fmt.Println(err)
		return
	}

	resp, err = Get(
		baseUrl+"/api/user/checkin",
		&RequestOptions{
			Headers: map[string]string{
				"Access-Token": data["result"].(map[string]interface{})["token"].(string),
			},
		},
	)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(string(resp.Content))
}
